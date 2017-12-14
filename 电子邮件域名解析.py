import dns.resolver

def resolve_hostname(hostname,indent=''):
    "打印出hostname对应的A记录或者AAAA记录；如果必要的话，跟踪CNAME指向的域名"
    indent = indent + '   '
    answer = dns.resolver.query(hostname,'A')
    if answer.rrset is not None:
        for record in answer:
            print(indent,hostname,'的IPv4（A）地址：',record.address)
        return
    answer = dns.resolver.query(hostname,'AAAA')
    if answer.rrset is not None:
        for record in answer:
            print(indent,hostname,'的IPv6（AAAA）地址：',record.address)
        return
    answer = dns.resolver.query(hostname,'CNAME')
    if answer.rrset is not None:
        record = answer[0]
        cname = record.address
        print(indent,hostname,'是个CNAME化名，指向了',cname)#?
        resolve_hostname(cname,indent)
        return
    print(indent,'ERROR:no A,AAAA,or CNAME record for',hostname)

def resolve_email_domain(domain):
    '对于一个地址为name@domain的邮箱，找到它的服务器IP地址'
    try:
        answer = dns.resolver.query(domain,'MX',raise_on_no_answer=False)
    except dns.resolver.NXDOMAIN:
        print('Error:No such domain',domain)
        return
    if answer.rrset is not None:
        records = sorted(answer,key=lambda  record:record.preference)
        for record in records:
            name = record.exchange.to_text(omit_final_dot=True)
            print('优先级：',record.preference)
            resolve_hostname(name)
    else:
        print('该域名没有明确的MX记录。')
        print('尝试将它作为一个A、AAAA、CNAME记录进行解析...')
        resolve_hostname(domain)

if __name__ == '__main__':

    while True:
        domain = input('输入想要解析的邮箱域名:')
        resolve_email_domain(domain)
        print()
