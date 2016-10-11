import chardet
import subprocess
SHOW_NETSH = 'netsh interface portproxy show all'
ADD = 'netsh interface portproxy add v4tov4 listenaddress=%s listenport=%s connectaddress=%s connectport=%s'
DEL = 'netsh interface portproxy delete v4tov4 listenaddress=%s listenport=%s'
CONSOLE = 'gb2312'


def execmd(SELECT):
    SELECT_LIST = SELECT.split()
    outer = subprocess.Popen(SELECT_LIST, stdout=subprocess.PIPE)
    outer_print = outer.stdout.read()
    ret = outer_print.decode(
        chardet.detect(outer_print)['encoding']).encode(CONSOLE)
    return ret


def add(local_ip, local_port, dest_ip, dest_port):
    ret = execmd(ADD % (local_ip, local_port, dest_ip, dest_port))
    print ret


def delete(local_ip, local_port):
    ret = execmd(DEL % (local_ip, local_port))
    print ret


def show():
    ret = execmd(SHOW_NETSH)
    ret = ret[ret.find('-\r\n') + 3:]
    ret = ret.split('\r\n')
    redict = {}
    idx = 1
    for i in ret:
        if i:
            istr = i.split()
            redict[str(idx)] = dict(local_ip=istr[0], local_port=istr[
                                    1], dest_ip=istr[2], dest_port=istr[3])
            idx += 1
    print '---------------------------------------------------'
    for i in redict:
        print '[%s] %16s:%5s >>> %16s:%5s ' % (i, redict[i]['local_ip'], redict[i]['local_port'], redict[i]['dest_ip'].ljust(16), redict[i]['dest_port'].ljust(16))
    print '---------------------------------------------------'
    return redict


def parser_cmd(ipt):
    slt = ipt.split()
    if not slt:
        slt.append('None')
    command = slt[0]
    slt = slt[1:]
    args, options, i = [], {}, 0
    while i < len(slt):
        if str(slt[i]).startswith('-'):
            if i + 1 < len(slt) and not str(slt[i + 1]).startswith('-'):
                options[str(slt[i])[1:]] = slt[i + 1]
                i += 1
            else:
                options[str(slt[i])[1:]] = True
        else:
            args.append(str(slt[i]))
        i += 1
    return command, args, options


def main():
    print '---------------------------------------------------'
    print 'add (local_ip) (local_port) (dest_ip) (dest_port)'
    print 'del (num)'
    print '---------------------------------------------------'
    this = show()
    while True:
        try:

            ipt = raw_input('>')
            command, args, options = parser_cmd(ipt)
            if command.lower() == 'add':
                add(*args)
            elif command.lower() == 'del':
                delete(this[args[0]]['local_ip'], this[args[0]]['local_port'])
            else:
                print 'ERROR INPUT'
            this = show()
        except Exception as ex:
            print 'ERROR', ex


if __name__ == '__main__':
    main()
