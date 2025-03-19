from abc import ABC,abstractmethod

class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self,amount):
        pass


class CreditCardPayment(PaymentStrategy):
    def pay(self,amount):
        print(f"amount paid using credit card {amount}")

class UPIPayment(PaymentStrategy):
    def pay(self, amount):
        print(f"paid using upi {amount}")

class PayPal(PaymentStrategy):
    def pay(self, amount):
        print(f"paid using paypal {amount}")


class PaymentProccessor:
    def __init__(self,startegy:PaymentStrategy):
        self.set_Strategy=startegy

    def setStrategy(self,strategy:PaymentStrategy):
        self.set_Strategy=strategy
    
    def make_payment(self,amount):
        self.set_Strategy.pay(amount)

if __name__=="__main__":
    processor=PaymentProccessor(CreditCardPayment())
    processor.make_payment(500)
    processor.setStrategy(PayPal())
    processor.make_payment(300)