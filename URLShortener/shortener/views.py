import json
from json.decoder import JSONDecodeError
from http import HTTPStatus

from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from shortener.models import URL
from shortener.utils import is_url_valid


def response_error(err_msg):
    return JsonResponse({'shorten_url': None, 'msg': err_msg},
                        status=HTTPStatus.BAD_REQUEST)


# TODO: add throttles for views

@csrf_exempt
@require_http_methods(['POST'])
def shorten_url(request):
    try:
        url = json.loads(request.body)['url']
    except JSONDecodeError:
        return response_error("Content type is application/json.")
    except KeyError:
        return response_error("Invalid payload.")

    url_valid, err_msg = is_url_valid(url)
    if not url_valid:
        return response_error(err_msg)

    hash = URL.objects.save_url(url)
    domain = request.META['HTTP_HOST']
    scheme = request.is_secure() and "https" or "http"
    shorten_url = f"{scheme}://{domain}/r/{hash}"

    return JsonResponse({'shorten_url': shorten_url, 'msg': None},
                        status=HTTPStatus.CREATED)


@require_http_methods(['GET'])
def redirect_view(request, hash):
    url = URL.objects.get_url(hash)
    if not url:
        return HttpResponse('<h1>Error: Unable to find URL to redirect to.</h1>')
    return redirect(url)

