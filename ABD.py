#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ABD.py — منسق ومعدل (نسخة محفوظة على سطح المكتب)
تغييرات: ترتيب أسطر، خطوط موحدة، لوحة ألوان جديدة، وإضافة ترقيم أسطر مبسط.
"""
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import subprocess
import sys
import os
import ast
import threading


class PythonCodeTester:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("أداة اختبار برامج Python")
        self.root.geometry("900x700")

        # لوحة ألوان حديثة
        self.bg_color = "#f8fafc"       # خلفية التطبيق
        self.panel_bg = "#ffffff"      # خلفية البطاقات
        self.text_bg = "#0b1220"       # خلفية منطقة النتائج (داكنة للقراءة)
        self.success_color = "#10b981"
        self.error_color = "#ef4444"
        self.warning_color = "#f59e0b"
        self.primary_btn = "#06b6d4"
        self.text_color = "#0f1724"

        self.root.configure(bg=self.bg_color)

        # إنشاء واجهة المستخدم
        self.create_widgets()

        # ملف Python المختار
        self.selected_file: str | None = None

    def create_widgets(self) -> None:
        # العنوان الرئيسي
        title_label = tk.Label(
            self.root,
            text="أداة اختبار برامج Python",
            font=("Segoe UI", 18, "bold"),
            bg=self.bg_color,
            fg=self.text_color,
        )
        title_label.pack(pady=10)

        # إطار التحميل
        upload_frame = tk.Frame(self.root, bg=self.bg_color)
        upload_frame.pack(pady=10, padx=20, fill="x")

        # زر تحميل الملف
        upload_btn = tk.Button(
            upload_frame,
            text="📁 اختر ملف Python",
            command=self.upload_file,
            font=("Segoe UI", 12),
            bg=self.primary_btn,
            fg="white",
            padx=15,
            pady=8,
        )
        upload_btn.pack(side="left", padx=10)

        # تسمية اسم الملف
        self.file_label = tk.Label(
            upload_frame,
            text="لم يتم اختيار أي ملف",
            font=("Segoe UI", 10),
            bg=self.bg_color,
            fg="#6b7280",
        )
        self.file_label.pack(side="left", padx=10)

        # إطار الاختبار
        test_frame = tk.Frame(self.root, bg=self.bg_color)
        test_frame.pack(pady=10, padx=20, fill="x")

        # زر تنفيذ الاختبار
        self.test_btn = tk.Button(
            test_frame,
            text="▶ تشغيل الاختبار",
            command=self.run_test,
            font=("Segoe UI", 14, "bold"),
            bg="#10b981",
            fg="white",
            padx=20,
            pady=10,
            state="disabled",
        )
        self.test_btn.pack(side="left", padx=10)

        # زر عرض الكود
        view_code_btn = tk.Button(
            test_frame,
            text="📝 عرض الكود",
            command=self.view_code,
            font=("Segoe UI", 12),
            bg="#7c3aed",
            fg="white",
            padx=15,
            pady=8,
            state="disabled",
        )
        view_code_btn.pack(side="left", padx=10)
        self.view_code_btn = view_code_btn

        # زر مسح النتائج
        clear_btn = tk.Button(
            test_frame,
            text="🗑️ مسح النتائج",
            command=self.clear_results,
            font=("Segoe UI", 12),
            bg="#ef4444",
            fg="white",
            padx=15,
            pady=8,
        )
        clear_btn.pack(side="right", padx=10)

        # علامات تبويب للنتائج
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, padx=20, fill="both", expand=True)

        # تبويب نتيجة الاختبار
        self.test_result_tab = tk.Frame(self.notebook, bg=self.panel_bg)
        self.notebook.add(self.test_result_tab, text="نتيجة الاختبار")

        # منطقة عرض نتيجة الاختبار
        self.result_text = scrolledtext.ScrolledText(
            self.test_result_tab,
            font=("Courier New", 10),
            bg=self.text_bg,
            fg=self.panel_bg,
            height=20,
            wrap="word",
        )
        self.result_text.pack(pady=10, padx=10, fill="both", expand=True)

        # تبويب عرض الكود
        self.code_view_tab = tk.Frame(self.notebook, bg=self.panel_bg)
        self.notebook.add(self.code_view_tab, text="عرض الكود")

        # منطقة عرض الكود
        self.code_text = scrolledtext.ScrolledText(
            self.code_view_tab,
            font=("Courier New", 10),
            bg=self.panel_bg,
            fg=self.text_color,
            height=20,
            wrap="word",
        )
        self.code_text.pack(pady=10, padx=10, fill="both", expand=True)

        # تبويب المعلومات
        self.info_tab = tk.Frame(self.notebook, bg=self.panel_bg)
        self.notebook.add(self.info_tab, text="معلومات الأداة")

        info_text = (
            """
        🛠️ أداة اختبار برامج Python

        هذه الأداة تسمح لك ب:
        1. تحميل ملفات Python (.py) لاختبارها
        2. التحقق من صحة الكود التركيبي (Syntax)
        3. اختبار تنفيذ البرنامج
        4. عرض الأخطاء مع تحديد مكانها
        5. عرض رسالة نجاح عند عدم وجود أخطاء

        ميزات الأداة:
        - واجهة مستخدم سهلة
        - فحص شامل للكود
        - عرض مفصل للأخطاء
        - عرض الكود المصدري
        - دعم ملفات متعددة
        """
        )

        info_label = tk.Label(
            self.info_tab,
            text=info_text,
            font=("Segoe UI", 11),
            bg=self.panel_bg,
            justify="right",
            anchor="w",
            fg=self.text_color,
        )
        info_label.pack(pady=20, padx=20, fill="both", expand=True)

        # شريط الحالة
        self.status_bar = tk.Label(
            self.root,
            text="جاهز - اختر ملف Python لبدء الاختبار",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            bg="#eef2ff",
            font=("Segoe UI", 9),
            fg=self.text_color,
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def upload_file(self) -> None:
        """تحميل ملف Python"""
        file_path = filedialog.askopenfilename(
            title="اختر ملف Python",
            filetypes=[("Python files", "*.py"), ("All files", "*.*")],
        )

        if file_path:
            self.selected_file = file_path
            file_name = os.path.basename(file_path)
            self.file_label.config(text=f"الملف المختار: {file_name}", fg=self.text_color)
            self.test_btn.config(state="normal")
            self.view_code_btn.config(state="normal")
            self.status_bar.config(text=f"تم تحميل الملف: {file_name}")

            # عرض محتوى الملف
            self.display_file_content(file_path)

    def display_file_content(self, file_path: str) -> None:
        """عرض محتوى الملف في تبويب الكود مع ترقيم أسطر مبسط"""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

            # إضافة أرقام الأسطر (مبسطة)
            lines = content.splitlines()
            numbered = "\n".join(f"{i+1:4d} | {line}" for i, line in enumerate(lines))

            self.code_text.delete(1.0, tk.END)
            self.code_text.insert(tk.END, numbered)

        except Exception as e:
            messagebox.showerror("خطأ", f"لا يمكن قراءة الملف: {str(e)}")

    def run_test(self) -> None:
        """تشغيل اختبار الكود"""
        if not self.selected_file:
            messagebox.showwarning("تحذير", "لم يتم اختيار أي ملف للاختبار")
            return

        # تفعيل وضع الانتظار
        self.test_btn.config(state="disabled", text="جاري الاختبار...")
        self.status_bar.config(text="جاري اختبار الكود...")
        self.result_text.delete(1.0, tk.END)

        # تشغيل الاختبار في thread منفصل لمنع تجميد الواجهة
        test_thread = threading.Thread(target=self.perform_test, daemon=True)
        test_thread.start()

    def perform_test(self) -> None:
        """تنفيذ اختبار الكود"""
        try:
            syntax_result = self.check_syntax()

            if not syntax_result["success"]:
                self.show_result("error", syntax_result["message"])
                self.root.after(0, self.enable_test_button)
                return

            execution_result = self.check_execution()
            if not execution_result["success"]:
                self.show_result("error", execution_result["message"])
                self.root.after(0, self.enable_test_button)
                return

            logic_result = self.check_basic_logic()
            if not logic_result["success"]:
                self.show_result("warning", logic_result["message"])
                self.root.after(0, self.enable_test_button)
                return

            success_message = (
                f"\n✅ تم اختبار الكود بنجاح!\n\nالملف: {os.path.basename(self.selected_file)}\n"
            )

            self.show_result("success", success_message)

        except Exception as e:
            error_message = f"حدث خطأ غير متوقع أثناء الاختبار: {str(e)}"
            self.show_result("error", error_message)

        finally:
            self.root.after(0, self.enable_test_button)

    def enable_test_button(self) -> None:
        """إعادة تفعيل زر الاختبار"""
        self.test_btn.config(state="normal", text="▶ تشغيل الاختبار")

    def check_syntax(self) -> dict:
        """فحص التركيب النحوي للكود"""
        try:
            with open(self.selected_file, "r", encoding="utf-8") as file:
                source_code = file.read()

            ast.parse(source_code)

            return {"success": True, "message": "التركيب النحوي للكود صحيح"}

        except SyntaxError as e:
            error_msg = (
                f"❌ خطأ في التركيب النحوي (Syntax Error):\n\n"
                f"نوع الخطأ: {e.msg}\n"
                f"الملف: {os.path.basename(self.selected_file)}\n"
                f"السطر: {e.lineno}\n"
                f"العمود: {e.offset}\n\n"
                f"السياق:\n{e.text or ''}\n"
            )

            return {"success": False, "message": error_msg}

    def check_execution(self) -> dict:
        """فحص تنفيذ البرنامج"""
        try:
            result = subprocess.run(
                [sys.executable, self.selected_file],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode == 0:
                output = result.stdout or "البرنامج نفذ بنجاح بدون إخراج"
                return {"success": True, "message": f"تم تنفيذ البرنامج بنجاح\n\nالإخراج:\n{output}"}
            else:
                error_msg = (
                    f"❌ خطأ أثناء التنفيذ:\n\nرمز الخطأ: {result.returncode}\n\n"
                    f"رسالة الخطأ:\n{result.stderr}\n\n"
                    f"الإخراج (إن وجد):\n{result.stdout}"
                )
                return {"success": False, "message": error_msg}

        except subprocess.TimeoutExpired:
            return {"success": False, "message": "❌ تجاوز البرنامج الوقت المحدد للتنفيذ (10 ثواني)."}
        except Exception as e:
            return {"success": False, "message": f"❌ حدث خطأ أثناء التنفيذ: {str(e)}"}

    def check_basic_logic(self) -> dict:
        """فحص منطق البرنامج الأساسي"""
        try:
            with open(self.selected_file, "r", encoding="utf-8") as file:
                source_code = file.read()

            checks = []

            if "def " in source_code:
                checks.append("✓ يحتوي على دوال معرّفة")
            else:
                checks.append("⚠️ لا يحتوي على دوال معرّفة")

            comment_count = source_code.count("#")
            if comment_count > 5:
                checks.append(f"✓ يحتوي على تعليقات كافية ({comment_count} تعليق)")
            elif comment_count > 0:
                checks.append(f"⚠️ يحتوي على تعليقات قليلة ({comment_count} تعليق)")
            else:
                checks.append("⚠️ لا يحتوي على تعليقات")

            if "try:" in source_code and "except" in source_code:
                checks.append("✓ يحتوي على معالجة أخطاء")
            else:
                checks.append("⚠️ لا يحتوي على معالجة أخطاء")

            if "print(" in source_code or "input(" in source_code:
                checks.append("✓ يحتوي على عمليات إدخال/إخراج")
            else:
                checks.append("⚠️ لا يحتوي على عمليات إدخال/إخراج واضحة")

            checks_text = "\n".join(checks)

            return {
                "success": True,
                "message": f"📊 فحص المنطق الأساسي:\n\n{checks_text}\n",
            }

        except Exception as e:
            return {"success": False, "message": f"❌ حدث خطأ أثناء الفحص المنطقي: {str(e)}"}

    def show_result(self, result_type: str, message: str) -> None:
        """عرض نتيجة الاختبار"""
        self.root.after(0, lambda: self._update_result_display(result_type, message))

    def _update_result_display(self, result_type: str, message: str) -> None:
        """تحديث عرض النتائج"""
        self.result_text.delete(1.0, tk.END)

        if result_type == "success":
            self.result_text.configure(bg=self.success_color, fg="#ffffff")
            self.status_bar.config(text="تم اختبار الكود بنجاح!")
            messagebox.showinfo("نجاح الاختبار", "تم اختبار الكود بنجاح!\n\nالبرنامج يعمل بشكل صحيح.")
        elif result_type == "error":
            self.result_text.configure(bg=self.error_color, fg="#ffffff")
            self.status_bar.config(text="تم اكتشاف أخطاء في الكود")
        elif result_type == "warning":
            self.result_text.configure(bg=self.warning_color, fg="#ffffff")
            self.status_bar.config(text="تم اكتشاف تحذيرات في الكود")

        self.result_text.insert(tk.END, message)
        self.notebook.select(0)

    def view_code(self) -> None:
        """عرض الكود"""
        if self.selected_file:
            self.notebook.select(1)
            self.status_bar.config(text="عرض محتوى الملف")

    def clear_results(self) -> None:
        """مسح النتائج"""
        self.result_text.delete(1.0, tk.END)
        self.result_text.configure(bg=self.text_bg, fg=self.panel_bg)
        self.status_bar.config(text="تم مسح النتائج")

        if self.selected_file:
            self.test_btn.config(state="normal")
        else:
            self.test_btn.config(state="disabled")


def main() -> None:
    root = tk.Tk()
    app = PythonCodeTester(root)

    # أيقونة (اختياري)
    try:
        root.iconbitmap("python_icon.ico")
    except Exception:
        pass

    root.mainloop()


if __name__ == "__main__":
    main()
