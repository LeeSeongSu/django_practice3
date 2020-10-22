from django.conf import settings
from django.db import models
from uuid import uuid4
from iamport import Iamport
from jsonfield import JSONField
import pytz
from datetime import datetime
from django.contrib.humanize.templatetags.humanize import intcomma
from django.utils.safestring import mark_safe
from django.http import Http404
# Create your models here.

def named_property(name):
    def wrap(fn):
        fn.short_description = name
        return property(fn)
    return wrap


def timestamp_to_datetime(timestamp):
    if timestamp:
        tz = pytz.timezone(settings.TIME_ZONE)
        return datetime.utcfromtimestamp(timestamp).replace(tzinfo=tz)
    return None


class Item(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField(blank=True)
    amount = models.PositiveIntegerField()
    photo = models.ImageField()
    date_select = models.DateTimeField(null=True,blank=True)
    is_public = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)
    username = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,default='')
    hashtag_field = models.CharField(max_length=200, blank=True) #해시태그
    #hashtags = models.ManyToManyField('Hashtag', blank=True) #해시태그
    place=models.CharField(max_length=200, blank=True) #장소
    rule=models.TextField(blank=True) #규칙
    max_p=models.PositiveIntegerField(default=1) #최대인원
    meet_id=models.PositiveIntegerField(default=0) #모임 고유번호
    member=models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="members") #모임인원
    other_id=models.PositiveIntegerField(default=0) #참가자 고유번호



class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    merchant_uid = models.UUIDField(default=uuid4, editable=False)
    imp_uid = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=100, verbose_name='상품명')
    amount = models.PositiveIntegerField(verbose_name='결제금액')
    status = models.CharField(
        max_length=9,
        choices=(
            ('ready', '미결제'),
            ('paid', '결제완료'),
            ('cancelled', '결제취소'),
            ('failed', '결제실패')
        ),
        default='ready',
        db_index=True)
    meta = JSONField(blank=True, default={})
    is_ready = property(lambda self: self.status == 'ready')
    is_paid = property(lambda self: self.status == 'paid')
    is_paid_ok = property(lambda self: self.status == 'paid' and self.amount == self.meta.get('amount'))
    is_cancelled = property(lambda self: self.status == 'cancelled')
    is_failed = property(lambda self: self.status == 'failed')
    receipt_url = named_property('영수증')(lambda self: self.meta.get('receipt_url'))
    cancel_reason = named_property('취소이유')(lambda self: self.meta.get('cancel_reason'))
    fail_reason = named_property('실패이유')(lambda self: self.meta.get('fail_reason', ''))
    paid_at = named_property('결제일시')(lambda self: timestamp_to_datetime(self.meta.get('paid_at')))
    failed_at = named_property('실패일시')(lambda self: timestamp_to_datetime(self.meta.get('failed_at')))
    cancelled_at = named_property('취소일시')(lambda self: timestamp_to_datetime(self.meta.get('cancelled_at')))

    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-id',)

    @property
    def api(self):
        'Iamport Client 인스턴스'
        return Iamport(settings.IAMPORT_API_KEY, settings.IAMPORT_API_SECRET)

    def update(self, commit=True, meta=None):
        '결재내역 갱신'
        if self.imp_uid:
            try:
                self.meta = meta or self.api.find(imp_uid=self.imp_uid)  # merchant_uid는 반드시 매칭되어야 합니다.
            except Iamport.HttpError:
                raise Http404('Not found {}'.format(self.imp_uid))

            assert str(self.merchant_uid) == self.meta['merchant_uid']
            self.status = self.meta['status']

            # 결제완료인데 가격비교 시 가격이 다른 경우 관리자 메시지 보내기
        if commit:
            self.save()

    @named_property('결제금액')
    def amount_html(self):
        return mark_safe('<div style="float: right;">{0}</div>'.format(intcomma(self.amount)))

    @named_property('처리결과')
    def status_html(self):
        cls, text_color = '', ''
        help_text = ''
        if self.is_ready:
            cls, text_color = 'fa fa-shopping-cart', '#ccc'
        elif self.is_paid_ok:
            cls, text_color = 'fa fa-check-circle', 'green'
        elif self.is_cancelled:
            cls, text_color = 'fa fa-times', 'gray'
            help_text = self.cancel_reason
        elif self.is_failed:
            cls, text_color = 'fa fa-ban', 'red'
            help_text = self.fail_reason

        html = '''
            <span style="color: {text_color};" title="this is title">
                <i class="{class_names}"></i>
                {label} </span>'''.format(class_names=cls, text_color=text_color, label=self.get_status_display())

        if help_text:
            html += '<br/>' + help_text
        return mark_safe(html)

    @named_property('영수증 링크')
    def receipt_link(self):
        if self.is_paid_ok and self.receipt_url:
            return mark_safe('<a href="{0}" target="_blank">영수증</a>'.format(self.receipt_url))

    def cancel(self, reason=None, commit=True):

        '결제내역 취소'
        if self.status == 'reserv':
            self.status = 'cancelled'
            self.meta['cancelled_at'] = int(time())
        try:
            commit = False
            meta = self.api.cancel(reason, imp_uid=self.imp_uid)
            assert str(self.merchant_uid) == self.meta['merchant_uid']
            self.update(commit=commit, meta=meta)
        # except Iamport.ResponseError as e:  # 취소시 오류 예외처리(이미 취소된 결제는 에러가 발생함)
        except:  # 취소시 오류 예외처리(이미 취소된 결제는 에러가 발생함)
            self.update(commit=commit)
        if commit:
            self.save()
