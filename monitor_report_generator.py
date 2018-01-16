import sys
from notification import Notification


def read_file(path):
    '''
    Read the file.

    :param param1: location of the file
    :returns: lines of file text
    '''
    with open(path, "r") as file:
        return file.read().splitlines()


def parsing_notification(file_content):
    '''
    Pre-process notifications.

    :param param1: file content
    :returns: array of notification objects
    :raise TypeError: unexpected data structure
    :raise ValueError: invalid timestamp
    '''
    notifications = []
    for line in file_content:
        # Trim whitespace
        line = line.strip()
        # Seperate elements by spaces
        elements = line.split(" ")
        try:
            # Store new notification object into array
            notifications.append(Notification(*elements))
        except TypeError:
            print "Unexpected data structure: " + line
            print "Exiting..."
            sys.exit()
        except ValueError:
            print "Invalid timestamp: " + line
            print "Exiting..."
            sys.exit()
    return notifications


def update_node_state(node_name, notification, nodes, mode):
    '''
    Update recent node status.

    :param param1: subject node name
    :param param2: the notification object that caused this update
    :param param3: status of nodes
    :param param4: ALIVE/DEAD update
    :returns: updated nodes
    '''
    
    if node_name is None:
        print "Missing subject: " + str(notification)
        print "Exiting..."
        sys.exit()
    # If new node
    elif node_name not in nodes:
        # Add the node directly with the state
        nodes[node_name] = {"notifications": [notification], "state": mode}
    else:
        # If previous node is in different state
        # AND that state is belongs to notification that
        # is within less than 50 milliseconds after this notification
        if nodes[node_name]["state"] != mode and \
                nodes[node_name]["notifications"][0].sent < notification.sent + 50:
            # Record this notification for later reference
            nodes[node_name]["notifications"].append(notification)
            # Set to UNKNOWN as could not tell which notification is first
            nodes[node_name]["state"] = "UNKNOWN"
    return nodes


def print_report(nodes):
    '''
    Generate/Print the final report.

    :param param1: status of nodes
    '''
    for name, node in nodes.iteritems():
        print name, node["state"], ', '.join(str(n) for n in node["notifications"])


def main(path):
    '''
    Main process.

    :param param1: location of the file
    '''

    # Get an array of all notifications
    notifications = parsing_notification(read_file(path))
    # Sort into decending order by the sent timestamp
    notifications.sort(reverse=True, key=lambda x: x.sent)
    # Dictionary of nodes status, which store another dictionary
    # {"notifications": [notification object, ...], "state": ALIVE/DEAD/UNKNOWN}
    nodes = {}

    for notification in notifications:
        if notification.action == "HELLO":
            # Means the sender is alive
            nodes = update_node_state(notification.sent_from, notification,
                                      nodes, "ALIVE")
        elif notification.action == "LOST":
            # Receieving this means sender is alive
            nodes = update_node_state(notification.sent_from, notification,
                                      nodes, "ALIVE")
            # The subject is dead
            nodes = update_node_state(notification.subject, notification,
                                      nodes, "DEAD")
        elif notification.action == "FOUND":
            # Receieving this means sender is alive
            nodes = update_node_state(notification.sent_from, notification,
                                      nodes, "ALIVE")
            # The subject is alive
            nodes = update_node_state(notification.subject, notification,
                                      nodes, "ALIVE")
        else:
            print "Unknown action: " + str(notification)
            print "Exiting..."
            sys.exit()

    print_report(nodes)


if __name__ == "__main__":
    if (len(sys.argv) >= 2):
        # Get file location
        main(sys.argv[1])
    else:
        print "Please specify the file, e.g. python monitor_report_generator fileName.txt"
