from app.core.error.message_codes import MessageCode


MESSAGES: dict[MessageCode, dict[str, str]] = {

    # =========================
    # SUCCESS
    # =========================
    MessageCode.RESOURCE_CREATED: {
        "en": "Resource created successfully",
        "ar": "تم إنشاء المورد بنجاح",
        "hi": "संसाधन सफलतापूर्वक बनाया गया",
    },

    MessageCode.OPERATION_SUCCESS: {
        "en": "Operation completed successfully",
        "ar": "تمت العملية بنجاح",
        "hi": "ऑपरेशन सफलतापूर्वक पूरा हुआ",
    },

    MessageCode.LOGIN_SUCCESS: {
        "en": "Login successful",
        "ar": "تم تسجيل الدخول بنجاح",
        "hi": "लॉगिन सफल हुआ",
    },

    MessageCode.LOGOUT_SUCCESS: {
        "en": "Logout successful",
        "ar": "تم تسجيل الخروج بنجاح",
        "hi": "लॉगआउट सफल हुआ",
    },

    MessageCode.DATA_FETCHED: {
        "en": "Data fetched successfully",
        "ar": "تم جلب البيانات بنجاح",
        "hi": "डेटा सफलतापूर्वक प्राप्त हुआ",
    },

    MessageCode.DATA_UPDATED: {
        "en": "Data updated successfully",
        "ar": "تم تحديث البيانات بنجاح",
        "hi": "डेटा सफलतापूर्वक अपडेट हुआ",
    },

    MessageCode.DATA_DELETED: {
        "en": "Data deleted successfully",
        "ar": "تم حذف البيانات بنجاح",
        "hi": "डेटा सफलतापूर्वक हटाया गया",
    },

    # =========================
    # VALIDATION
    # =========================
    MessageCode.VALIDATION_ERROR: {
        "en": "Validation error",
        "ar": "خطأ في التحقق من الصحة",
        "hi": "मान्यता त्रुटि",
    },

    MessageCode.INVALID_INPUT: {
        "en": "Invalid input provided",
        "ar": "تم تقديم إدخال غير صالح",
        "hi": "अमान्य इनपुट प्रदान किया गया",
    },

    MessageCode.REQUIRED_FIELD_MISSING: {
        "en": "Required field is missing",
        "ar": "الحقل المطلوب مفقود",
        "hi": "आवश्यक फ़ील्ड गायब है",
    },

    # =========================
    # AUTH
    # =========================
    MessageCode.INVALID_CREDENTIALS: {
        "en": "Invalid credentials",
        "ar": "بيانات اعتماد غير صالحة",
        "hi": "अमान्य क्रेडेंशियल",
    },

    MessageCode.UNAUTHORIZED_ACCESS: {
        "en": "Unauthorized access",
        "ar": "وصول غير مصرح به",
        "hi": "अनधिकृत पहुंच",
    },

    MessageCode.ACCESS_DENIED: {
        "en": "Access denied",
        "ar": "تم رفض الوصول",
        "hi": "पहुंच अस्वीकृत",
    },

    MessageCode.TOKEN_EXPIRED: {
        "en": "Token has expired",
        "ar": "انتهت صلاحية الرمز",
        "hi": "टोकन समाप्त हो गया है",
    },

    MessageCode.INVALID_TOKEN: {
        "en": "Invalid token",
        "ar": "رمز غير صالح",
        "hi": "अमान्य टोकन",
    },

    MessageCode.SESSION_INVALID: {
        "en": "Session is invalid",
        "ar": "الجلسة غير صالحة",
        "hi": "सेशन अमान्य है",
    },
    MessageCode.USERNAME_EXISTS: {
        "en": "User with this username already exists",
        "ar": "المستخدم موجود بالفعل بنفس اسم المستخدم",
        "hi": "इस उपयोगकर्ता का उपयोगकर्ता आईडी पहले से मौजूद है",
    },

    # =========================
    # SYSTEM
    # =========================
    MessageCode.RESOURCE_NOT_FOUND: {
        "en": "Requested resource not found",
        "ar": "المورد المطلوب غير موجود",
        "hi": "अनुरोधित संसाधन नहीं मिला",
    },

    MessageCode.CONFLICT_ERROR: {
        "en": "Conflict occurred",
        "ar": "حدث تعارض",
        "hi": "संघर्ष उत्पन्न हुआ",
    },

    MessageCode.INTERNAL_ERROR: {
        "en": "Internal server error",
        "ar": "خطأ داخلي في الخادم",
        "hi": "आंतरिक सर्वर त्रुटि",
    },

    MessageCode.SERVICE_UNAVAILABLE: {
        "en": "Service temporarily unavailable",
        "ar": "الخدمة غير متاحة مؤقتًا",
        "hi": "सेवा अस्थायी रूप से अनुपलब्ध है",
    },
}