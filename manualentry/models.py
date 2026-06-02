from django.db import models
from django.conf import settings  # CustomUser এর জন্য settings.AUTH_USER_MODEL ব্যবহার করা সেফ

# 🛡️ আপনার দেওয়া কমন অডিট অবজেক্ট ট্র্যাক ফ্রেমওয়ার্ক
class AuditModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Time")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Time")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="%(class)s_created",
        verbose_name="Created By"
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="%(class)s_updated",
        verbose_name="Updated By"
    )

    class Meta:
        abstract = True

# ১. Terminal Model
class Terminal(AuditModel):
    # ID অটোমেটিক জেনারেট হবে (Django default), আলাদা করে লিখার প্রয়োজন নেই।
    code = models.CharField(max_length=50, unique=True, verbose_name="Terminal Code")
    value = models.CharField(max_length=255, verbose_name="Value")
    description = models.TextField(null=True, blank=True, verbose_name="Description")

    def __str__(self):
        return f"{self.code} - {self.value}"

from django.core.exceptions import ValidationError

class ManualEntry(AuditModel):  # AuditModel ইনহেরিট করা থাকলো
    first_entry = models.IntegerField(default=0)
    second_entry = models.IntegerField(default=0)
    default_entry = models.IntegerField(default=1)
    total_terminal = models.ForeignKey(Terminal, on_delete=models.SET_NULL, null=True, blank=True)

    # Helper method to sanitize inputs
    def _get_cleaned_vals(self):
        return self.first_entry or 0, self.second_entry or 0, self.default_entry or 0

    # Formula 1: (1st - 2nd) - 1
    @property
    def f1_val(self):
        first, second, default = self._get_cleaned_vals()
        return (first - second) - default

    # Formula 2: (1st - 2nd)
    @property
    def f2_val(self):
        first, second, _ = self._get_cleaned_vals()
        return first - second

    # Formula 3: (1st - 2nd) + 1
    @property
    def f3_val(self):
        first, second, default = self._get_cleaned_vals()
        return (first - second) + default

    # Formula 4: (1st + 2nd) - 1
    @property
    def f4_val(self):
        first, second, default = self._get_cleaned_vals()
        return (first + second) - default

    # Formula 5: (1st + 2nd) + 1
    @property
    def f5_val(self):
        first, second, default = self._get_cleaned_vals()
        return (first + second) + default

    # 🎯 ব্যাকএন্ড ম্যাট্রিক্স ইন্টিগ্রিটি ভ্যালিডেশন ইঞ্জিন
    def clean(self):
        super().clean()
        
        # যদি ইউজার কোনো টার্মিনাল সিলেক্ট করে থাকে তবেই কেবল ভ্যালিডেশন রান হবে
        if self.total_terminal:
            # ৫টি ফর্মুলার মান স্ট্রিং ফরম্যাটে একটি লিস্টে নেওয়া হলো
            valid_outputs = [
                str(self.f1_val).strip(),
                str(self.f2_val).strip(),
                str(self.f3_val).strip(),
                str(self.f4_val).strip(),
                str(self.f5_val).strip()
            ]

            # টার্মিনাল অবজেক্টের 'code' ফিল্ডের মান নেওয়া হলো (বা আপনার মডেলে যে ফিল্ডটি আছে, যেমন: name বা terminal_id)
            # যদি টার্মিনাল মডেলে কোড ফিল্ডের নাম 'code' না হয়ে অন্য কিছু হয়, তবে self.total_terminal.code পরিবর্তন করুন
            terminal_code = str(self.total_terminal.code).strip() if hasattr(self.total_terminal, 'code') else str(self.total_terminal).strip()

            # আসল চেক: টার্মিনাল কোডটি কি আমাদের ৫টি ফর্মুলার যেকোনো একটির সাথে মিলে?
            if terminal_code not in valid_outputs:
                raise ValidationError({
                    'total_terminal': f"Data Mismatch! The selected Terminal code '{terminal_code}' "
                                      f"does not match any of the 5 matrix formula calculations {valid_outputs}."
                })

    def save(self, *args, **kwargs):
        # সেভ করার আগে ফুল ক্লিন মেথড কল করা নিশ্চিত করা হলো
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Entry #{self.id} - F1:{self.f1_val} | F2:{self.f2_val} | F3:{self.f3_val} | F4:{self.f4_val} | F5:{self.f5_val}"
    first_entry = models.IntegerField(default=0)
    second_entry = models.IntegerField(default=0)
    default_entry = models.IntegerField(default=1)
    total_terminal = models.ForeignKey(Terminal, on_delete=models.SET_NULL, null=True, blank=True)

    # Helper method to sanitize inputs
    def _get_cleaned_vals(self):
        return self.first_entry or 0, self.second_entry or 0, self.default_entry or 0

    # Formula 1: (1st - 2nd) - 1
    @property
    def f1_val(self):
        first, second, default = self._get_cleaned_vals()
        return (first - second) - default

    # Formula 2: (1st - 2nd)
    @property
    def f2_val(self):
        first, second, _ = self._get_cleaned_vals()
        return first - second

    # Formula 3: (1st - 2nd) + 1
    @property
    def f3_val(self):
        first, second, default = self._get_cleaned_vals()
        return (first - second) + default

    # Formula 4: (1st + 2nd) - 1
    @property
    def f4_val(self):
        first, second, default = self._get_cleaned_vals()
        return (first + second) - default

    # Formula 5: (1st + 2nd) + 1
    @property
    def f5_val(self):
        first, second, default = self._get_cleaned_vals()
        return (first + second) + default

    def __str__(self):
        return f"Entry #{self.id} - F1:{self.f1_val} | F2:{self.f2_val} | F3:{self.f3_val} | F4:{self.f4_val} | F5:{self.f5_val}"