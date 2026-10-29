import json
import logging
import secrets
import subprocess
import time

from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods

from .ai_buddy import execute_system_action, get_destructive_action, process_input

logger = logging.getLogger(__name__)


@require_http_methods(["GET"])
def wish_me(request):
    """Redirect to the browser-based assistant interface."""
    return redirect("home-page")


@ensure_csrf_cookie
@require_http_methods(["GET", "POST"])
def home(request):
    """Render the assistant or process text recognized/provided by the browser."""
    if request.method == "GET":
        return render(request, "tenali/home.html")

    try:
        payload = json.loads(request.body) if request.content_type == "application/json" else request.POST.dict()
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "Invalid JSON request body."}, status=400)

    if not isinstance(payload, dict):
        return JsonResponse({"error": "Request body must be an object."}, status=400)

    if "confirmation_token" in payload:
        return _handle_confirmation(request, payload)

    user_input = payload.get("text")
    if not isinstance(user_input, str) or not user_input.strip():
        return JsonResponse({"error": "A non-empty text value is required."}, status=400)
    user_input = user_input.strip()
    if len(user_input) > 2000:
        return JsonResponse({"error": "Text must be 2000 characters or fewer."}, status=400)

    action = get_destructive_action(user_input)
    if action:
        token = secrets.token_urlsafe(32)
        request.session["pending_destructive_action"] = {
            "action": action,
            "token": token,
            "created_at": time.time(),
        }
        action_label = "shut down" if action == "shutdown" else "restart"
        return JsonResponse({
            "user_input": user_input,
            "response": f"Please confirm if you want to {action_label} this computer.",
            "confirmation_required": True,
            "confirmation_token": token,
        })

    try:
        response = process_input(user_input)
        logger.info("Processed browser input: %s -> %s", user_input, response)
        return JsonResponse({"user_input": user_input, "response": response})
    except Exception as e:
        logger.error("Unexpected error processing browser input: %s", e, exc_info=True)
        return JsonResponse({"error": "The request could not be processed."}, status=500)


def _handle_confirmation(request, payload):
    pending = request.session.get("pending_destructive_action")
    token = payload.get("confirmation_token")

    if not isinstance(token, str) or not isinstance(pending, dict):
        return JsonResponse({"error": "No pending action matches this confirmation."}, status=400)
    if not secrets.compare_digest(token, pending.get("token", "")):
        return JsonResponse({"error": "No pending action matches this confirmation."}, status=400)

    if time.time() - pending.get("created_at", 0) > 60:
        del request.session["pending_destructive_action"]
        return JsonResponse({"error": "Confirmation expired. Please request the action again."}, status=400)

    confirmed = payload.get("confirm")
    if not isinstance(confirmed, bool):
        return JsonResponse({"error": "A boolean confirmation value is required."}, status=400)

    del request.session["pending_destructive_action"]
    if not confirmed:
        return JsonResponse({"response": "System action canceled."})

    try:
        response = execute_system_action(pending.get("action"))
    except (OSError, subprocess.SubprocessError, ValueError):
        logger.exception("Confirmed system action failed: %s", pending.get("action"))
        return JsonResponse({"error": "The confirmed system action could not be executed."}, status=500)
    return JsonResponse({"response": response})
