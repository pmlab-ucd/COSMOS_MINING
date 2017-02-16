from sensitive_component import SensitiveComponent

# Here's our "unit".
def IsOdd(n):
    return n % 2 == 1


# Here's our "unit tests".
class SensitiveComponentTests:

    @staticmethod
    def simplify_name_test(method_name):
        print(SensitiveComponent.SensEntryPoint.simplify_name(method_name))


if __name__ == '__main__':
    SensitiveComponentTests.simplify_name_test('com.seattleclouds.modules.rateandreview.a: void onClick(android.view.View)>')
    SensitiveComponentTests.simplify_name_test('<com.Vertifi.Mobile.Deposit.SubmittedDepositsActivity: android.view.View onCreateView(java.lang.String,android.content.Context,android.util.AttributeSet)>')
