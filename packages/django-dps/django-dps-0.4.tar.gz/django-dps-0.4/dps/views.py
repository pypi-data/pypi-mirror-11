from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.http import HttpResponseForbidden
from pprint import pformat
from django.http import Http404
from django.shortcuts import render_to_response

from .decorators import dps_result_view
from .models import Transaction


@dps_result_view
def transaction_success(request, token, result=None):
    # Check the transaction was actually successful, since there's nothing
    # to stop DPS or whoever requesting the "success" url for a failed
    # transaction
    if not result:
        raise Http404('Could not retrieve transaction')
    if result['Success'] != '1':
        return HttpResponseForbidden('Transaction was unsuccessful')

    transaction = get_object_or_404(Transaction,
                                    status__in=[Transaction.PROCESSING,
                                                Transaction.SUCCESSFUL],
                                    secret=token)
    transaction.result_dict = result
    transaction.save()

    status_updated = transaction.set_status(Transaction.SUCCESSFUL)

    # if we're recurring, we need to save the billing token now.
    content_object = transaction.content_object
    if content_object.is_recurring():
        content_object.set_billing_token(result["DpsBillingId"] or None)

    # callback, if it exists. It may optionally return a url for redirection
    success_url = getattr(content_object,
                          "transaction_succeeded",
                          lambda *args: None)(transaction, True,
                                              status_updated)

    if success_url:
        # assumed to be a valid url
        return HttpResponseRedirect(success_url)
    else:
        return render_to_response("dps/transaction_success.html", {
                    "request": request,
                    "transaction": transaction})


@dps_result_view
def transaction_failure(request, token, result=None):
    # Check the transaction actually failed, since there's nothing
    # to stop DPS or whoever requesting the "failure" url for a successful
    # transaction
    if not result:
        raise Http404('Could not retrieve transaction')
    if result['Success'] != '0':
        return HttpResponseForbidden('Transaction was successful')

    transaction = get_object_or_404(Transaction,
                                    status__in=[Transaction.PROCESSING,
                                                Transaction.FAILED],
                                    secret=token)
    transaction.result_dict = result
    transaction.save()

    status_updated = transaction.set_status(Transaction.FAILED)

    content_object = transaction.content_object

    # callback, if it exists. It may optionally return a url for redirection
    failure_url = getattr(content_object,
                          "transaction_failed",
                          lambda *args: None)(transaction, True,
                                              status_updated)

    if failure_url:
        # assumed to be a valid url
        return HttpResponseRedirect(failure_url)
    else:
        return render_to_response("dps/transaction_failure.html", {
                "request": request,
                "transaction": transaction})
