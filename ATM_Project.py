from tkinter import messagebox
import customtkinter as ctk
import pyrebase


class ATM:
    def __init__(self):
        self.withdraw_window = None
        self.deposit_window = None
        firebaseConfig = {
            'apiKey': "AIzaSyBBTKH9WY_49zU72Om2ddC7OTLLm06mRV0",
            'authDomain': "atm-project-8234b.firebaseapp.com",
            'databaseURL': "https://atm-project-8234b-default-rtdb.asia-southeast1.firebasedatabase.app",
            'projectId': "atm-project-8234b",
            'storageBucket': "atm-project-8234b.appspot.com",
            'messagingSenderId': "861526836309",
            'appId': "1:861526836309:web:70b3b0c471761affca00dc",
            'measurementId': "G-36ZDPDHP37"
        }
        firebase = pyrebase.initialize_app(firebaseConfig)
        self.database = firebase.database()

        self.data = {}
        self.app = ctk.CTk()
        self.app.title("Main window")
        self.app.geometry("600x600")
        wlcm_msg = ctk.CTkLabel(self.app, text= "Welcome to ATM Service", font=("Arial", 50))
        wlcm_msg.pack(pady=50)
        login_btn = ctk.CTkButton(self.app, text="Log in", font=("Oswald", 40), command=self.Log_In_window, width=200, height=80)
        login_btn.pack(pady=20)
        reg_btn = ctk.CTkButton(self.app, text="Register Your Account", font=("Oswald", 40), command=self.Registration_window, width=200, height=80)
        reg_btn.pack(pady=10)
        self.app.mainloop()

    def Registration_window(self):
        reg_window = ctk.CTkToplevel()
        reg_window.geometry("600x500")
        reg_window.title("Register")
        reg_window.grab_set()
        login_head = ctk.CTkLabel(reg_window, text="Enter Your Details", font=("Oswald", 40))
        login_head.grid(row=0, column=0, pady=30, columnspan=4, padx=50)

        acc_no_label = ctk.CTkLabel(reg_window, text="Enter Your Account No: ", font=("Oswald", 20))
        acc_no_label.grid(row=1, column=0, pady=10, padx=40)
        self.acc_no_entry = ctk.CTkEntry(reg_window, font=("Oswald", 20), width=200)
        self.acc_no_entry.grid(row=1, column=2, pady=10, padx=20)

        label_name = ctk.CTkLabel(reg_window, text="Name: ", font=("Oswald", 20))
        label_name.grid(row=2, column=0, pady=10,padx=40)
        self.name = ctk.CTkEntry(reg_window, font=("Oswald", 20), width=200)
        self.name.grid(row=2, column=2, pady=10,padx=20)

        label_email = ctk.CTkLabel(reg_window, text="Email ", font=("Oswald", 20))
        label_email.grid(row=3, column=0, pady=10,padx=40)
        self.email_entry = ctk.CTkEntry(reg_window, font=("Oswald", 20), width=200)
        self.email_entry.grid(row=3, column=2, pady=10,padx=20)

        label_pin = ctk.CTkLabel(reg_window, text="Set Your PIN: ", font=("Oswald", 20))
        label_pin.grid(row=4, column=0, pady=10,padx=40)
        self.pin = ctk.CTkEntry(reg_window, font=("Oswald", 20), width=200, show="*")
        self.pin.grid(row=4, column=2, pady=10, padx=20)

        log_in_btn = ctk.CTkButton(reg_window, text="Submit", font=("Oswald", 50), height= 30, width= 230, command=self.Regestration_track)
        log_in_btn.grid(row=5, columnspan=5, pady=10,padx=20)


    def Log_In_window(self):
        login_window = ctk.CTkToplevel()
        login_window.geometry("500x500")
        login_window.title("Log In")
        login_window.grab_set()

        login_head = ctk.CTkLabel(login_window, text="Enter Your Details",  font=("Oswald", 40))
        login_head.grid(row=0, column = 0, pady=30,  columnspan=4, padx=50)

        label_name = ctk.CTkLabel(login_window, text="Enter Your Account No: ", font=("Oswald", 20))
        label_name.grid(row=1, column=0, pady=10,padx=40)
        self.acc_no_entry = ctk.CTkEntry(login_window, font=("Oswald", 20), width=170)
        self.acc_no_entry.grid(row=1, column=2, pady=10,padx=20)

        label_pin = ctk.CTkLabel(login_window, text="Enter Your PIN: ", font=("Oswald", 20))
        label_pin.grid(row=2, column=0, pady=10,padx=40)
        self.pin = ctk.CTkEntry(login_window, font=("Oswald", 20), width=170, show="*")
        self.pin.grid(row=2, column=2, pady=10, padx=20)

        log_in_btn = ctk.CTkButton(login_window, text="Submit", font=("Oswald", 50), height= 30, width= 230, command=self.services_window)
        log_in_btn.grid(row=4, columnspan=5, pady=10,padx=20)



    def Regestration_track(self):
        self.data.update({"account_no": self.acc_no_entry.get(), "email": self.email_entry.get(), "name": self.name.get(), "pin_code": self.pin.get(), "balance": 0 })
        existing_account = self.database.child("Registered Users").child(self.acc_no_entry.get()).get(self.data["account_no"])
        print(existing_account.val())
        if existing_account.val() is None :
            self.database.child("Registered Users").child(self.data["account_no"]).set(self.data)
            messagebox.showinfo("Success", "Your Account Registered for ATM Services")
        else:
            messagebox.showerror(title="Error", message=f"Account No : '{self.data["account_no"]}' is already Registered ")


    def services_window(self):
        acc_no = self.acc_no_entry.get()
        pin = self.pin.get()

        user_detail = self.database.child("Registered Users").child(acc_no).get()
        user_pin = self.database.child("Registered Users").child(acc_no).child("pin_code").get()
        if user_detail is not None:
            if user_pin.val() == pin:
                messagebox.showinfo(title="Success", message="Login Success")
                self.transaction_window = ctk.CTkToplevel()
                self.transaction_window.geometry("500x600")
                self.transaction_window.title("Services Window")
                self.transaction_window.grab_set()
                trans_option = ctk.CTkLabel(self.transaction_window, text="ATM Services",  font=("Oswald", 40))
                trans_option.grid(row=0, column = 2, pady=30, columnspan=2, padx=150, sticky="n")

                check_bal_btn = ctk.CTkButton(self.transaction_window, text="Check Balance", font=("Oswald", 20), height=70 ,command=self.check_balance)
                check_bal_btn.grid(row=3, column=2, pady=10, padx=10, columnspan=5)

                deposit_btn = ctk.CTkButton(self.transaction_window, text="Deposit Cash", font=("Oswald", 20), height=70, command=self.deposit_cash)
                deposit_btn.grid(row=4, column=2, pady=10, padx=10, columnspan=5)

                withdraw_btn = ctk.CTkButton(self.transaction_window, text="Withdraw Cash", font=("Oswald", 20), height=70, command=self.withdraw_cash)
                withdraw_btn.grid(row=5, column=2, pady=10, padx=10, columnspan=5)

                change_pin_btn = ctk.CTkButton(self.transaction_window, text="Change PIN", font=("Oswald", 20), height=70, command=self.click_pin_Change)
                change_pin_btn.grid(row=6, column=2, pady=10, padx=10, columnspan=5)

                exit_btn = ctk.CTkButton(self.transaction_window, text="Exit",  font=("Oswald", 20), height=70, command=self.exit)
                exit_btn.grid(row=7, column=2, pady=10, padx=10, columnspan=5)
            else:
                messagebox.showerror("Error", message="Wrong PIN.")
        else:
            messagebox.showerror(title="Error", message= "Account is not Registered")



    def check_balance(self):
        existing_account = self.database.child("Registered Users").child(self.acc_no_entry.get()).child("balance").get()
        current_bal = existing_account.val()
        bal_window = ctk.CTkToplevel()
        bal_window.geometry("500x500")
        bal_window.title("Balance")
        bal_window.grab_set()
        current_balance = ctk.CTkLabel(bal_window, text=f"Your Current Balance is\n '{current_bal}'", font=("Oswald", 40))
        current_balance.grid(row=3, column=0, columnspan=5, pady=30, padx=30)
        tran_window = ctk.CTkButton(bal_window, text="Back to Transaction Window", command=bal_window.destroy)
        tran_window.grid(row=5, column=0, columnspan=3, pady=40, padx=40)

    def click_deposit(self):

        deposit_entry = self.deposit_entry.get()
        existing_account = self.database.child("Registered Users").child(self.acc_no_entry.get()).child("balance").get()
        current_bal = existing_account.val()
        current_bal += int(deposit_entry)
        self.database.child("Registered Users").child(self.acc_no_entry.get()).update({"balance": current_bal})
        show_deposit = ctk.CTkLabel(self.deposit_window, text=f"Deposited Cash '{deposit_entry}'. Your current balance is '{current_bal}'")
        show_deposit.grid(row=5, column=0, columnspan=5, pady=30, padx=30)
        tran_window = ctk.CTkButton(self.deposit_window,text="Back to Transaction Window", command=self.deposit_window.destroy)
        tran_window.grid(row=9, column=0, columnspan=3, pady=40, padx=40)


    def deposit_cash(self):

        self.deposit_window = ctk.CTkToplevel()
        self.deposit_window.geometry("500x500")
        self.deposit_window.title("Deposit Cash")
        self.deposit_window.grab_set()
        deposit_label = ctk.CTkLabel(self.deposit_window, text="Enter Deposit Amount: ", font=("Oswald", 20))
        deposit_label.grid(row=0, column=0, pady=30, padx=30)
        self.deposit_entry = ctk.CTkEntry(self.deposit_window, font=("Oswald", 20), width=150)
        self.deposit_entry.grid(row=0, column=1, pady=30, padx=30)
        deposit_btn = ctk.CTkButton(self.deposit_window, text="Deposit", font=("Oswald", 40), command=self.click_deposit)
        deposit_btn.grid(row=4, column=0, columnspan=3, pady=40)

    def click_withdraw(self):

        existing_account = self.database.child("Registered Users").child(self.acc_no_entry.get()).child("balance").get()
        current_bal = existing_account.val()
        withdraw_entry = self.withdraw_entry.get()
        if int(withdraw_entry) > current_bal:
            show_withdraw = ctk.CTkLabel(self.withdraw_window, text=f"Insufficient balance for transaction.\n Your current balance is: '{current_bal}'")
            show_withdraw.grid(row=5, column=0, columnspan=5, pady=30, padx=30)
        else:
            current_bal -= int(withdraw_entry)
            self.database.child("Registered Users").child(self.acc_no_entry.get()).update({"balance": current_bal})
            show_transacted_withdraw = ctk.CTkLabel(self.withdraw_window, text=f"Withdraw Cash '{withdraw_entry}'.\n Your current balance is '{current_bal}'")
            show_transacted_withdraw.grid(row=5, column=0, columnspan=5, pady=30, padx=30)
        tran_window = ctk.CTkButton(self.withdraw_window, text="Back to Transaction Window", command=self.withdraw_window.destroy)
        tran_window.grid(row=6, column=0, columnspan=3, pady=40, padx=40)

    def withdraw_cash(self):

        self.withdraw_window =ctk.CTkToplevel()
        self.withdraw_window.geometry("500x570")
        self.withdraw_window.title("Withdraw Cash")
        self.withdraw_window.grab_set()
        withdraw_label = ctk.CTkLabel(self.withdraw_window, text="Enter Withdraw Amount: ", font=("Oswald", 20))
        withdraw_label.grid(row=0, column=0, pady=30, padx=30)
        self.withdraw_entry = ctk.CTkEntry(self.withdraw_window, font=("Oswald", 20), width=150)
        self.withdraw_entry.grid(row=0, column=1, pady=30, padx=30)
        withdraw_btn = ctk.CTkButton(self.withdraw_window, text="Withdraw", font=("Oswald", 40), command=self.click_withdraw)
        withdraw_btn.grid(row=4, column=0, columnspan=3, pady=40)

    def click_pin_Change(self):
        self.change_pin_window = ctk.CTkToplevel()
        self.change_pin_window.geometry("500x500")
        self.change_pin_window.title("Change PIN")
        self.change_pin_window.grab_set()

        old_pin_label = ctk.CTkLabel(self.change_pin_window, text="Enter old PIN", font=("Oswald", 20))
        old_pin_label.grid(row=0, column=0, pady=30, padx=30)
        self.old_pin_entry = ctk.CTkEntry(self.change_pin_window, font=("Oswald", 20), width=150)
        self.old_pin_entry.grid(row=0, column=1, pady=30, padx=30)

        new_pin_label = ctk.CTkLabel(self.change_pin_window, text="Set New PIN", font=("Oswald", 20))
        new_pin_label.grid(row=2, column=0, pady=30, padx=30)
        self.new_pin_entry = ctk.CTkEntry(self.change_pin_window, font=("Oswald", 20), width=150)
        self.new_pin_entry.grid(row=2, column=1, pady=30, padx=30)

        change_pin_btn = ctk.CTkButton(self.change_pin_window, text="Change PIN Code", height=70 , font=("Oswald", 20), command=self.change_pin)
        change_pin_btn.grid(row=4, column=0, columnspan=3, pady=40)

        tran_window = ctk.CTkButton(self.change_pin_window, text="Back to Transaction Window", command=self.change_pin_window.destroy)
        tran_window.grid(row=5, column=0, columnspan=3, pady=40, padx=40)

    def change_pin(self):

        old_pin = self.old_pin_entry.get()
        new_pin = self.new_pin_entry.get()
        old_pin_fb = self.database.child("Registered Users").child(self.acc_no_entry.get()).child("pin_code").get()
        if old_pin_fb.val() == old_pin:
            self.database.child("Registered Users").child(self.acc_no_entry.get()).update({"pin_code": new_pin})
            messagebox.showinfo("Success", message="Password Updated Successfully")
        else:
            messagebox.showerror("Error", message="Old Password is not correct")

    def exit(self):
        res = messagebox.askquestion(title="Exit", message="Do you want to exit?")
        if res == "yes":
            self.transaction_window.destroy()
        else:
            pass



root = ATM()