# PurchaseCoin

Run FlaskFrameworkMining.py as a python app in console to start your own node.

You may open it to the internet, but most of my experiments have been over LAN.

Running a blockchain in python is not recommended. One of the largest problems of Bitcoin is that proof of work is extremely inefficient,
  and python runs at 50x's the powerdraw of most C++ applications, such as Bitcoin.

To do:<br />
  prevent easy main chain takeover by larger chains
  

to resolve conflicts, you must make sure all nodes have registered all other nodes
    you must register each node with each other one<br />
    ex:<br />
       make sure 0.0.0.0:0000 knows itself and any other nodes exist<br /><br />
    Makes the longest chain the new head, just like Bitcoin<br />
        The block after the genesis block becomes that of the node with longest chain<br />
    
