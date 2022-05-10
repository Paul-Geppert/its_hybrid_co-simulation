#include <errno.h>
#include <string.h>
#include <stdlib.h>

#include <asn_application.h>
#include <asn_internal.h>

#define PDU_Type_Ptr    NULL

typedef struct conversionResult
{
    size_t size;
    void * buffer;
} conversionResult;

// For external use
conversionResult * encodeToXer(int messageId, int protocolVersion, char * file, int length);
void freeConversionResult(conversionResult * ptr);

// For internal use
static asn_TYPE_descriptor_t * _getPduType(int messageId, int protocolVersion);
static void * _decode_to_pdu_from_buffer(asn_TYPE_descriptor_t *pduType, char* file, int length);

// PDUs are defined in pdu_collection.c
extern asn_TYPE_descriptor_t *asn_pdu_collection_v1[];
extern asn_TYPE_descriptor_t *asn_pdu_collection_v2[];

//////////////////// PUBLIC ////////////////////

conversionResult * encodeToXer(int messageId, int protocolVersion, char * buffer, int length) {
    asn_TYPE_descriptor_t * pduType = _getPduType(messageId, protocolVersion);

    conversionResult * conversionError = malloc(sizeof(conversionResult));
    conversionError->size = -1;
    conversionError->buffer = NULL;

    // Unknown PDU type
    if (pduType == PDU_Type_Ptr) {
        fprintf(stderr, "Could not find PDU type with id '%d' for version '%d'\n", messageId, protocolVersion);
        return conversionError;
    }

    void * structure = _decode_to_pdu_from_buffer(pduType, buffer, length);

    if (structure == 0) {
        fprintf(stderr, "Failed to decode data\n");
        return conversionError;
    }

    asn_encode_to_new_buffer_result_t encodingResult = asn_encode_to_new_buffer(0, ATS_BASIC_XER, pduType, structure);

    ASN_STRUCT_FREE(*pduType, structure);

    if (encodingResult.result.encoded < 0) {
        fprintf(stderr, "Failed to encode data to XER, failed on %s: %s\n", encodingResult.result.failed_type->name, strerror(errno));
        return conversionError;
    }

    // Reuse already allocated memory
    conversionResult * encodedAnswer = conversionError;
    encodedAnswer->size = encodingResult.result.encoded;
    encodedAnswer->buffer = encodingResult.buffer;

    return encodedAnswer;
}

void freeConversionResult(conversionResult * ptr) {
    if (ptr->buffer) {
        free(ptr->buffer);
    }
    free(ptr);
}

//////////////////// INTERNAL ////////////////////

static asn_TYPE_descriptor_t * _getPduType(int messageId, int protocolVersion) {
    asn_TYPE_descriptor_t **pdu = 0;
    asn_TYPE_descriptor_t *pduType = PDU_Type_Ptr;

    if (protocolVersion == 1) {
        pdu = asn_pdu_collection_v1;
    }
    else if (protocolVersion == 2) {
        pdu = asn_pdu_collection_v2;
    }

    if (pdu == 0 || messageId < 0 || messageId > 255) {
        return pduType;
    }

    pduType = pdu[messageId];

    return pduType;
}

static void * _decode_to_pdu_from_buffer(asn_TYPE_descriptor_t *pduType, char* data, int length) {
    asn_codec_ctx_t *opt_codec_ctx = 0;
    void *structure = 0;
    asn_dec_rval_t rval;

    if (!data) {
        fprintf(stderr, "No data data provided\n");
        return 0;
    }

    if (!pduType) {
        fprintf(stderr, "PDU type cannot be NULL\n");
        return 0;
    }

    rval = uper_decode(opt_codec_ctx, pduType, (void **)&structure, data, length, 0, 0);

    free(opt_codec_ctx);

    if (rval.code == RC_OK) {
        return structure;
    }

    ASN_STRUCT_FREE(*pduType, structure);

    ASN_DEBUG("Decode failed: %s\n",
                (rval.code == RC_WMORE)
                ? "Unexpected end of input"
                : "Input processing error");

#ifndef ENOMSG
#define ENOMSG EINVAL
#endif
#ifndef EBADMSG
#define EBADMSG EINVAL
#endif
    
    errno = (rval.code == RC_WMORE) ? ENOMSG : EBADMSG;

    fprintf(stderr, "Failed to decode data with given PDU type: %s\n", strerror(errno));

    return 0;
}
