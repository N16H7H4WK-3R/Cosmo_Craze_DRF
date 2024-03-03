from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    access_token = refresh.access_token
    access_token_lifetime = access_token.lifetime.total_seconds()
    # Convert seconds to Days, Hours, Minutes, and Seconds
    days, remainder = divmod(access_token_lifetime, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    expires_in = f"{int(days)}d:{int(hours)}h:{int(minutes)}m:{int(seconds)}s"
    return {
        "refresh": str(refresh),
        "access": str(access_token),
        "expires_in": expires_in,
    }
