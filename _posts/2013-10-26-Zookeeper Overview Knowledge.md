---
layout: post
date: 2014-07-30
title: Zookeeper Overview Knowledge
---

What is Zookeeper
====================
> ZooKeeper is a distributed, open-source coordination service for distributed applications. It exposes a simple set of primitives that distributed applications can build upon to implement higher level services for synchronization, configuration maintenance, and groups and naming. It is designed to be easy to program to, and uses a data model styled after the familiar directory tree structure of file systems. It runs in Java and has bindings for both Java and C. Coordination services are notoriously hard to get right. They are especially prone to errors such as race conditions and deadlock. The motivation behind ZooKeeper is to relieve distributed applications the responsibility of implementing coordination services from scratch.

Design Goals
=====================
* ZooKeeper is simple.

 > **ZooKeeper allows distributed processes to coordinate with each other through a shared hierarchal namespace which is organized similarly to a standard file system. The name space consists of data registers - called znodes**, in ZooKeeper parlance - and these are similar to files and directories. Unlike a typical file system, which is designed for storage, ZooKeeper data is kept in-memory, which means ZooKeeper can achieve high throughput and low latency numbers. The ZooKeeper implementation puts a premium on high performance, highly available, strictly ordered access. The performance aspects of ZooKeeper means it can be used in large, distributed systems. The reliability aspects keep it from being a single point of failure. The strict ordering means that sophisticated synchronization primitives can be implemented at the client.

* ZooKeeper is replicated. 

 > Like the distributed processes it coordinates, ZooKeeper itself is intended to be replicated over a sets of hosts called an ensemble.
	
 >	![] (/images/zookeeper-overview-knowledge/zkservice.jpg)
 
 > The servers that make up the ZooKeeper service must all know about each other. They maintain an in-memory image of state, along with a transaction logs and snapshots in a persistent store. As long as a majority of the servers are available, the ZooKeeper service will be available. Clients connect to a single ZooKeeper server. The client maintains a TCP connection through which it sends requests, gets responses, gets watch events, and sends heart beats. If the TCP connection to the server breaks, the client will connect to a different server.

* ZooKeeper is ordered. 

 > ZooKeeper stamps each update with a number that reflects the order of all ZooKeeper transactions. Subsequent operations can use the order to implement higher-level abstractions, such as synchronization primitives.

* ZooKeeper is fast. 
 
 > It is especially fast in "read-dominant" workloads. ZooKeeper applications run on thousands of machines, and it performs best where reads are more common than writes, at ratios of around 10:1.
	
Data model and the hierarchical namespace
==========================================

> **The name space provided by ZooKeeper is much like that of a standard file system.** A name is a sequence of path elements separated by a slash (/). Every node in ZooKeeper's name space is identified by a path.

> ![] (/images/zookeeper-overview-knowledge/zknamespace.jpg)

> * Nodes and ephemeral nodes

    > **Unlike is standard file systems, each node in a ZooKeeper namespace can have data associated with it as well as children.** It is like having a file-system that allows a file to also be a directory. (ZooKeeper was designed to store coordination data: status information, configuration, location information, etc., so the data stored at each node is usually small, in the byte to kilobyte range.) We use the term znode to make it clear that we are talking about ZooKeeper data nodes. **Znodes maintain a stat structure that includes version numbers for data changes, ACL changes, and timestamps, to allow cache validations and coordinated updates. Each time a znode's data changes, the version number increases.** For instance, whenever a client retrieves data it also receives the version of the data. The data stored at each znode in a namespace is read and written atomically. Reads get all the data bytes associated with a znode and a write replaces all the data. Each node has an Access Control List (ACL) that restricts who can do what. ZooKeeper also has the notion of ephemeral nodes. These znodes exists as long as the session that created the znode is active. When the session ends the znode is deleted.

> * Conditional updates and watches

  > ZooKeeper supports the concept of watches. Clients can set a watch on a znodes. A watch will be triggered and removed when the znode changes. When a watch is triggered the client receives a packet saying that the znode has changed. And if the connection between the client and one of the Zoo Keeper servers is broken, the client will receive a local notification. 

> * Implementation

  > ZooKeeper Components shows the high-level components of the ZooKeeper service. With the exception of the request processor, each of the servers that make up the ZooKeeper service replicates its own copy of each of components.

  > ![] (/images/zookeeper-overview-knowledge/zkcomponents.jpg)

	> * The replicated database is an in-memory database containing the entire data tree. Updates are logged to disk for recoverability, and writes are serialized to disk before they are applied to the in-memory database. 
	> * Every ZooKeeper server services clients. Clients connect to exactly one server to submit irequests. 
	  > * Read requests are serviced from the local replica of each server database. 
		> * Requests that change the state of the service, write requests, are processed by an agreement protocol. As part of the agreement protocol all write requests from clients are forwarded to a single server, called the leader. The rest of the ZooKeeper servers, called followers, receive message proposals from the leader and agree upon message delivery. The messaging layer takes care of replacing leaders on failures and syncing followers with leaders. ZooKeeper uses a custom atomic messaging protocol. Since the messaging layer is atomic, ZooKeeper can guarantee that the local replicas never diverge. When the leader receives a write request, it calculates what the state of the system is when the write is to be applied and transforms this into a transaction that captures this new state.
		
> * Guarantees
  
  > ZooKeeper is very fast and very simple. Since its goal, though, is to be a basis for the construction of more complicated services, such as synchronization, it provides a set of guarantees. These are:
	1 Sequential Consistency - Updates from a client will be applied in the order that they were sent.
	2 Atomicity - Updates either succeed or fail. No partial results.
	3 Single System Image - A client will see the same view of the service regardless of the server that it connects to.
	4 Reliability - Once an update has been applied, it will persist from that time forward until a client overwrites the update.
	5 Timeliness - The clients view of the system is guaranteed to be up-to-date within a certain time bound.

  * Simple API

One of the design goals of ZooKeeper is provide a very simple programming interface. As a result, it supports only these operations:
	1 Create - creates a node at a location in the tree
	2 Delete - deletes a node
	3 Exists - tests if a node exists at a location
	4 get data - reads the data from a node
	5 set data - writes data to a node
	6 get children - retrieves a list of children of a node
	7 Sync - waits for data to be propagated

  * Performance

ZooKeeper is designed to be highly performant. But is it? The results of the ZooKeeper's development team at Yahoo! Research indicate that it is. (See ZooKeeper Throughput as the Read-Write Ratio Varies.) It is especially high performance in applications where reads outnumber writes, since writes involve synchronizing the state of all servers. (Reads outnumbering writes is typically the case for a coordination service.)


Zookeeper Setup in Distribute Mode
=================================
* Prerequisites:
1. Java must be installed.
2. IPTables must be off/stop on all  nodes.

* How to setup:

Use below steps to install zookeeper in distributed mode:
	1. Download zookeeper recent stable release  on each machine.
	2. Extract it and set Environment variable ZOOKEEPER_HOME to root directory of zookeeper.
	3. Define configuration in conf/zoo.cfg file
	```
  tickTime=2000
	dataDir=/var/zookeeper/
	clientPort=2181
	initLimit=5
	syncLimit=2
	server.1=zoo1:2888:3888
	server.2=zoo2:2888:3888
	server.3=zoo3:2888:3888
	```
	The new entry, initLimit is timeouts ZooKeeper uses to limit the length of time the ZooKeeper servers in quorum have to connect to a leader. The entry syncLimit limits how far out of date a server can be from a leader. With both of these timeouts, you specify the unit of time using tickTime. In this example, the timeout for initLimit is 5 ticks at 2000 milleseconds a tick, or 10 seconds. The entries of the form server.X list the servers that make up the ZooKeeper service. When the server starts up, it knows which server it is by looking for the file myid in the data directory. That file has the contains the server number, in ASCII. Finally, note the two port numbers after each server name: " 2888" and "3888". Peers use the former port to connect to other peers. Such a connection is necessary so that peers can communicate, for example, to agree upon the order of updates. More specifically, a ZooKeeper server uses this port to connect followers to the leader. When a new leader arises, a follower opens a TCP connection to the leader using this port. Because the default leader election also uses TCP, we currently require another port for leader election. This is the second port in the server entry. 
	
	**Note:** If one machine will have more than one zookeeper instance then their client port must be different 2181, 2182 and also their server’s port must be different:
	```
	server.1=zoo1:2888:3888
	server.2=zoo1:2889:3889
	server.3=zoo3:2888:3888
	```
	**Note 1:** Each zookeeper in ensemble will have same server’s configuration.
	**Note 2:** Data directory path(dataDir) must be specified to an existing directory.

	4. Define server id: Server id can be defined by creating a file named myid, one for each server, which resides in that server's data directory, as specified by the configuration file parameter dataDir. The myid file consists of a single line containing only the text of that machine's id. So myid of server 1 would contain the text "1" and nothing else. The id must be unique within the ensemble. This step must be performed very carefully because there is most chances we make error and then waste lots of time to measure why our cluster is not running properly.
	5. Start  Zookeeper:
	Now we can start each zookeeper node by running following command:
	```$ZOOKEEPER_HOME/bin/zkServer.sh start```
	6. Check the status of each node:
	```$ZOOKEEPER_HOME/bin/zkServer.sh status```

Now our zookeeper cluster is ready to use.

