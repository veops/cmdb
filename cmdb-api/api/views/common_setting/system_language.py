import os

from api.resource import APIView
from api.lib.perm.auth import auth_abandoned

prefix = "/system"


class SystemLanguageView(APIView):
    url_prefix = (f"{prefix}/language",)

    method_decorators = []

    @auth_abandoned
    def get(self):
        """Get system default language
        Read from environment variable SYSTEM_DEFAULT_LANGUAGE, default to Chinese if not set
        """
        default_language = os.environ.get("SYSTEM_DEFAULT_LANGUAGE", "")

        return self.jsonify(
            {
                "language": default_language,
                "language_name": self._get_language_name(default_language),
            }
        )

    def _get_language_name(self, language_code):
        """Return language name based on language code"""
        language_mapping = {
            "zh-CN": "中文(简体)",
            "zh-TW": "中文(繁体)",
            "en-US": "English",
            "ja-JP": "日本語",
            "ko-KR": "한국어",
        }
        return language_mapping.get(language_code, "")
