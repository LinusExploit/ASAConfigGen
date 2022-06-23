# This is a sample Python script.
import random
import string
import re

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
ips = ['1.1.1.1', '1.1.1.2', '1.1.1.3', '1.1.1.4'
       ]

octets = [str(x) for x in range(0, 255)]
ports = [str(x) for x in range(20, 6500)]


def dump_config_gen():
    for ip in ips:
        for i in range(2, 65000):
            print(
                'access-list acl_out extended permit tcp host {} object-group DM_INLINE_NETWORK_12 eq {}'.format(ip, i))


def gen_rand_ip():
    # This is a function that generates a random ip string
    ipl = [(random.choice(octets)),
           (random.choice(octets)),
           (random.choice(octets)),
           (random.choice(octets))
           ]

    return '.'.join(ipl)


def gen_rand_service():
    # This is a function that generates a random service
    service = (random.choice(ports))
    return service


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return "malhyari_" + result_str


def gen_object_network():
    return """object network {}
    host {}
    """.format(get_random_string(4), gen_rand_ip())


def gen_object_group_network():
    return """object-group network {}
    network-object host {}
    network-object host {}
    network-object host {}
    """.format(get_random_string(4), gen_rand_ip(), gen_rand_ip(), gen_rand_ip())


def gen_object_group_service_tcp():
    return """object-group service {} tcp
    port-object eq {}
    port-object eq {}
    port-object eq {}
    """.format(get_random_string(4), gen_rand_service(), gen_rand_service(), gen_rand_service())


def gen_object_group_service_udp():
    return """object-group service {} udp
    port-object eq {}
    port-object eq {}
    port-object eq {}
    """.format(get_random_string(4), gen_rand_service(), gen_rand_service(), gen_rand_service())


def gen_config():
    # This function will generate the random configuration
    # first generate 5000 objects of type network
    acls = []
    object_networks = []
    for i in range(0, 5000):
        object_networks.append(gen_object_network())

    # Second we generate 5000 objects of type groups
    object_network_groups = []
    for i in range(0, 5000):
        object_network_groups.append(gen_object_group_network())

    # Third is to  generate 1000 object groups  of type service for tcp
    object_service_tcp_groups = []
    for i in range(0, 1000):
        object_service_tcp_groups.append(gen_object_group_service_tcp())

    # Third is to  generate 500 object groups  of type service for udp
    object_service_udp_groups = []
    for i in range(0, 1000):
        object_service_udp_groups.append(gen_object_group_service_udp())

    for i in range(1, 1000):
        # different source, same destination, same service 100 times tcp
        for x in range(0, 30):
            acls.append('access-list acl_out extended permit tcp object-group {} object-group {} object-group {}'\
                        .format(re.findall(r'^[\w-]+\s\w+\s(\w+$)', random.choice(object_network_groups), re.MULTILINE)[0],\
                        re.findall(r'^[\w-]+\s\w+\s(\w+$)', object_network_groups[i], re.MULTILINE)[0],\
                        re.findall(r'^[\w-]+\s\w+\s(\w+)\stcp$', object_service_tcp_groups[i], re.MULTILINE)[0]))

        # different source, same destination, same service 100 times udp
        for x in range(0, 30):
            acls.append('access-list acl_out extended permit udp object-group {} object-group {} object-group {}'\
                        .format(re.findall(r'^[\w-]+\s\w+\s(\w+$)', random.choice(object_network_groups), re.MULTILINE)[0],\
                        re.findall(r'^[\w-]+\s\w+\s(\w+$)', object_network_groups[i], re.MULTILINE)[0],\
                        re.findall(r'^[\w-]+\s\w+\s(\w+)\sudp$', object_service_udp_groups[i], re.MULTILINE)[0]))

        # same source, same destination, different service 100 times tcp
        for x in range(0, 30):
            acls.append('access-list acl_out extended permit tcp object-group {} object-group {} object-group {}'\
                        .format(re.findall(r'^[\w-]+\s\w+\s(\w+$)', object_network_groups[i], re.MULTILINE)[0],\
                        re.findall(r'^[\w-]+\s\w+\s(\w+$)', object_network_groups[i], re.MULTILINE)[0],\
                        re.findall(r'^[\w-]+\s\w+\s(\w+)\stcp$', random.choice(object_service_tcp_groups), re.MULTILINE)[0]))

        # different source, different destination, different service 100 times tcp
        for x in range(0, 60):
            acls.append('access-list acl_out extended permit tcp object-group {} object-group {} object-group {}'\
                        .format(re.findall(r'^[\w-]+\s\w+\s(\w+$)', random.choice(object_network_groups), re.MULTILINE)[0],\
                        re.findall(r'^[\w-]+\s\w+\s(\w+$)', random.choice(object_network_groups), re.MULTILINE)[0],\
                        re.findall(r'^[\w-]+\s\w+\s(\w+)\stcp$', random.choice(object_service_tcp_groups), re.MULTILINE)[0]))

    return object_networks,object_network_groups,object_service_tcp_groups,object_service_udp_groups,acls


def main():
    # print(gen_rand_ip())
    # print(gen_rand_service())
    # print(gen_object_group_network())
    # print(gen_object_group_service_tcp())
    # print(gen_object_group_service_udp())
    # print(gen_object_network())
    object_networks_out, object_network_groups_out, object_service_tcp_groups_out, object_service_udp_groups_out, acls_out = gen_config()

    for line in object_service_tcp_groups_out:
        print(line)

    for line in object_service_udp_groups_out:
        print(line)

    for line in object_networks_out:
        print(line)

    for line in object_network_groups_out:
        print(line)

    for line in acls_out:
        print(line)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
