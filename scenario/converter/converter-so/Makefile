CFLAGS += $(ASN_MODULE_CFLAGS) -DASN_PDU_COLLECTION -I ../generated-v1 -I ../generated-v2
ASN_LIBRARIES ?= ../generated-v1/libasncodec.a ../generated-v2/libasncodec.a
ASN_PROGRAM ?= converter
ASN_PROGRAM_SRCS ?= ./converter.c \
	pdu_collection_v1.c \
	pdu_collection_v2.c

.PHONY: clean

all: $(ASN_PROGRAM)

$(ASN_PROGRAM): $(ASN_LIBRARIES) $(ASN_PROGRAM_SRCS:.c=.o)
	$(CC) $(CFLAGS) $(CPPFLAGS) -o $(ASN_PROGRAM) $(ASN_PROGRAM_SRCS:.c=.o) $(LDFLAGS) $(ASN_LIBRARIES) $(LIBS)

.SUFFIXES: .c .o

.c.o:
	$(CC) $(CFLAGS) -o $@ -c $<

clean:
	rm -f $(ASN_PROGRAM)
	rm -f $(ASN_MODULE_SRCS:.c=.o) $(ASN_PROGRAM_SRCS:.c=.o)
