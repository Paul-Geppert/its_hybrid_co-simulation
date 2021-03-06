/*
 * Generated by asn1c-0.9.29 (http://lionet.info/asn1c)
 */

#include "../generated-v2/CAM.h"
#include "../generated-v2/DENM.h"
#include "../generated-v2/MAPEM.h"
#include "../generated-v2/SPATEM.h"
#include "../generated-v2/SREM.h"
#include "../generated-v2/SSEM.h"

struct asn_TYPE_descriptor_s;	/* Forward declaration */

struct asn_TYPE_descriptor_s *asn_pdu_collection_v2[] = {
	// 0 - is not specified
	0,
	// 1 - DENM - From module DENM-PDU-Descriptions in ./v1/DENM.asn
	&asn_DEF_DENM,	
	// 2 - CAM - From module CAM-PDU-Descriptions in ./v1/CAM.asn
	&asn_DEF_CAM,	
	// 3 - POI
	0,
	// 4 - SPATEM - From module SPATEM-PDU-Descriptions in ./v1/SPATEM.asn
	&asn_DEF_SPATEM,
	// 5 - MAPEM - From module MAPEM-PDU-Descriptions in ./v1/MAPEM.asn
	&asn_DEF_MAPEM,	
	// 6 - IVIM
	0,
	// 7 - EV-RSR
	0,
	// 8 - tistpgtransaction
	0,
	// 9 - SREM - From module SREM-PDU-Descriptions in ./v1/SREM.asn
	&asn_DEF_SREM,	
	// 10 - SSEM - From module SSEM-PDU-Descriptions in ./v1/SSEM.asn
	&asn_DEF_SSEM,	
	// 11 - EVCSN
	// 12 - SAEM
	// 13 - RTCMEM
	[11 ... 255] = 0
};

