from opcua import Client

OPC_ADDRESS = "opc.tcp://192.168.0.1:4840"


def browse_nodes():
    client = Client(OPC_ADDRESS)
    try:
        client.connect()
        root = client.get_root_node()
        print("Root Node: ", root)

        # Hole den 'Objects' Knoten (häufig der Startpunkt für alle Geräte)
        objects = client.get_objects_node()
        print("Objects Node: ", objects)

        # Durchlaufe alle direkten Childs des Objects-Knotens
        children = objects.get_children()
        for child in children:
            print("Knoten: ", child, " - Node-ID: ", child.nodeid)

    except Exception as e:
        print("Fehler beim Browsen: ", e)
    finally:
        client.disconnect()


if __name__ == "__main__":
    browse_nodes()
