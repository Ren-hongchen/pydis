from pydis import PydisObject ,PydisObjectEncodingEnum



def sds_encoded_object(obj: PydisObject) -> bool:
    return (obj.encoding == PydisObjectEncodingEnum.PYDIS_ENCODING_RAW) \
           or (obj.encoding == PydisObjectEncodingEnum.PYDIS_ENCODING_EMBSTR)

def compare_string_objects(a_obj: PydisObject, b_obj: PydisObject) -> int:
    if a_obj is b_obj:
        return 0

    if sds_encoded_object(a_obj):
        a_str = a_obj.ptr.data
    else:
        a_str = str(a_obj.ptr)

    if sds_encoded_object(b_obj):
        b_str = b_obj.ptr.data
    else:
        b_str = str(b_obj.ptr)

    if a_str < b_str:
        return -1
    elif a_str > b_str:
        return 1
    else:
        return 0

def equal_string_objects(a_obj: PydisObject, b_obj: PydisObject) -> bool:
    if a_obj.encoding == b_obj.encoding == PydisObjectEncodingEnum.PYDIS_ENCODING_INT:
        return a_obj.ptr == b_obj.ptr
    else:
        return compare_string_objects(a_obj, b_obj) == 0
