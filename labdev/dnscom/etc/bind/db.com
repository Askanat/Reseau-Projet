$TTL	60000
@		IN	SOA	dnscom.com.	root.dnscom.com. (
			1 ; serial
			28 ; refresh
			14 ; retry
			3600000 ; expire
			60000 ; negative cache ttl
			)
@		IN	NS	dnscom.com.
dnscom		IN	A	42.13.37.42

perdu		IN	NS	dnsperdu.perdu.com.
dnsperdu.perdu	IN	A	8.8.8.8

rr		IN	NS	dnsrr.rr.com.
dnsrr.rr	IN	A	22.9.17.92


