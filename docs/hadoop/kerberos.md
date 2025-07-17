![Steps](kerberos.svg)

### **Explaination part 1**
Kerberos is a protocol designed to provide secure authentication to services over an insecure network. It ensures that passwords are never sent across the network and encryption keys are never directly exchanged. Furthermore, you and the application can mutually authenticate each other. Many organizations utilize Kerberos as the foundation for single sign-on capabilities. The name "Kerberos" originates from Greek mythology, specifically from Cerberus, the three-headed dog that guards the gates to the underworld, symbolizing its role in guarding access to applications.

To understand Kerberos, several key terms are essential:

   A Kerberos realm is the domain or group of systems where Kerberos has the authority to authenticate users to services. Multiple realms can exist and be interconnected.

   A principle is a unique identity, which can be either a user or a service (like an application).

   A client is a process that accesses a service on behalf of a user, essentially the user wanting to access something.

   A service is a resource provided to a client, such as a file server or an application.

   The Key Distribution Center (KDC) is the central component of Kerberos, responsible for supplying tickets and generating temporary session keys that enable secure user authentication to a service. The KDC stores all the secret symmetric keys for users and services. It comprises two main servers: the Authentication Server (AS) and the Ticket Granting Server (TGS).

   The Authentication Server (AS) confirms that a known user is making an access request and issues a Ticket Granting Ticket (TGT).

   The Ticket Granting Server (TGS) confirms that a user is requesting access to a known service and issues service tickets.

   Authenticators are records that contain information provably generated recently using a session key known only to the client and the server, facilitating mutual authentication.

   Tickets contain crucial information such as the client's identity, service ID, session keys, timestamps, and time to live, all encrypted with a server's secret key.

The high-level communication process for a user to access a service involves a series of messages exchanged between the user, the Authentication Server (AS), the Ticket Granting Server (TGS), and the service itself, with at least two messages sent at almost every step, some in plaintext and some encrypted with a symmetric key.

Here's a detailed breakdown of the Kerberos authentication process:

1.  Initial Request to Authentication Server (AS): The user initiates the process by sending an unencrypted message to the AS. This message includes the user's ID (e.g., Rob), the ID of the service they wish to access (e.g., a CRM application), the user's IP address (which can be single, multiple, or none, depending on configuration), and the requested lifetime for the TGT. While users might desire an infinite lifetime for convenience, security considerations often lead Kerberos to override such requests.

2.  AS Processing and Response: Upon receiving the user's message, the AS first verifies the user ID against its list of known users and their secret keys, retrieving the user's secret client key if found. The AS then generates two messages to send back to the user. The first message contains the ID of the TGS, the message creation timestamp, and its lifetime. The second message is the Ticket Granting Ticket (TGT), which includes the user's ID, the TGS's ID, a timestamp, the user's IP address, and the TGT's lifetime (which may differ from the user's request). The AS also generates a randomly generated symmetric TGS session key and adds it to both messages. The first message is encrypted with the user's secret key, and the TGT is encrypted with the TGS's secret key. These two encrypted messages are then sent to the user.

3.  User Processing AS Response: The user must decrypt the first message to proceed. This is done by the user generating their secret key, which involves entering their password. Kerberos adds a salt (typically the user's username at realm name) and a key version number (KDN) to the password. The salted password is then processed through a hashing algorithm (specifically, string-to-key) to generate the user's secret key. This key is used to decrypt the first message, and this decryption step also serves to validate the user's password; an incorrect password would result in a decryption failure. If successful, the user gains access to the TGS's ID and the TGS session key. Importantly, the user cannot decrypt the TGT because they do not possess the TGS's secret key.

4.  User Request to Ticket Granting Server (TGS): The user then prepares two new messages. The first is a simple plaintext message indicating the desired service and its requested ticket lifetime. The second is a user Authenticator, containing the user ID and a creation timestamp, encrypted with the TGS session key. These new messages, along with the still-encrypted TGT, are sent to the TGS.

5.  TGS Processing User Request: The TGS starts by examining the plaintext service ID and verifying it against its list of known services in the KDC, retrieving the service's secret key if found. The TGS then decrypts the TGT using its own secret key, which reveals the TGS session key. This session key is then used to decrypt the user Authenticator. With both the TGT and Authenticator decrypted, the TGS performs several validations: ensuring user IDs match between the TGT and Authenticator, comparing timestamps (tolerating up to a two-minute difference), comparing the TGT's IP address to the user's received IP address (if applicable), and checking if the TGT has expired. For replay protection, the TGS maintains a cache of recently received authenticators and checks if the current Authenticator is already in the cache; if not, it adds it.

6.  TGS Response to User: If all validations pass, the TGS creates two messages for the user. The first message includes the service ID, timestamp, and message lifetime. The second message is the service ticket, containing the user ID, the service ID, a timestamp, the user's IP address, and the service ticket's lifetime. The TGS generates a random symmetric service session key and adds it to both messages. The first message is encrypted with the TGS session key, and the service ticket is encrypted with the service secret key. These two messages are then sent to the user.

7.  User Processing TGS Response: The user decrypts the first message using the TGS session key (which they received from the AS), gaining access to the service session key. The user then creates a new Authenticator message with their ID and a timestamp, encrypting it with the service session key. The user cannot decrypt the service ticket because it's encrypted with the service's secret key, so they simply forward the encrypted service ticket along with the newly created Authenticator message to the service.

8.  Service Processing User Request: The service decrypts the service ticket using its own secret key, which reveals the service session key. This service session key is then used to decrypt the user Authenticator message. Similar to the TGS, the service performs validations: matching user IDs, comparing timestamps (tolerating less than two minutes difference), checking IP addresses, and verifying ticket expiration. For replay protection, the service also maintains a cache of recently received authenticators and adds the current one if it's new.

9.  Service Response and Mutual Authentication: If validations are successful, the service creates its own Authenticator message, including its service ID and a timestamp, encrypted with the service session key. This service Authenticator is sent back to the user. The user decrypts this message using the same symmetric service session key. The user then verifies that the service name in the Authenticator matches the expected service, completing the mutual authentication. The user also checks the timestamp to ensure the Authenticator was recently created. Finally, the user caches a copy of the encrypted service ticket for future use with that service, given the mutual authentication. This entire exchange securely distributes a symmetric service session key that allows the user and service to communicate authentication information securely.


### **Explaination part 2**

![Steps](kerberos.svg)

Kerberos is a network authentication protocol created by MIT that Hadoop uses for authentication and identity propagation. Hadoop needed a network-based authentication system because it operates across multiple computers and operating systems, unlike OS authentication which is limited to a single machine. The Hadoop community chose to integrate with an existing system like Kerberos rather than developing a built-in authentication capability. Kerberos was selected over other options like SSL certificates due to its better performance and simpler user management; for instance, removing a user in Kerberos involves a simple deletion, whereas revoking an SSL certificate is a more complicated process. A key benefit of Kerberos is that it eliminates the need for passwords to be transmitted across the network, thereby removing the potential threat of attackers "sniffing" or intercepting passwords.

To understand how Kerberos works, it's important to know its core components and terminology:

Key Distribution Center (KDC): This is the authentication server in a Kerberos environment, often residing on a separate physical server. The KDC is logically divided into three parts:

Database: This part stores user and service identities, which are known as principles. It also holds other information like encryption keys, ticket validity durations, and expiration dates.

Authentication Server (AS): The AS is responsible for authenticating users. If a user's credentials are valid, the AS issues a Ticket Granting Ticket (TGT). Having a valid TGT means the authentication server has verified your identity.

Ticket Granting Server (TGS): The TGS is essentially the application server of the KDC. Before accessing any service within a Hadoop cluster, you need to obtain a service ticket from the TGS.

Here's a detailed breakdown of how Kerberos authenticates a user attempting to access a service in a Hadoop cluster, such as listing a directory from HDFS:

1.  Initial Authentication (User to KDC - AS): The process begins on a Linux machine where the user executes the `kinit` tool. The `kinit` program prompts for the user's password and then sends an authentication request to the Kerberos Authentication Server (AS). Upon successful authentication, the AS responds by providing a Ticket Granting Ticket (TGT). The `kinit` tool then stores this TGT in the user's credentials cache. At this point, the user has been authenticated and is ready to execute a Hadoop command.

2.  Requesting a Service Ticket (Hadoop Client to KDC - TGS): When a user runs a Hadoop command (e.g., `hadoop fs -ls /`), the Hadoop client uses the cached TGT to contact the Ticket Granting Server (TGS). The client approaches the TGS to request a service ticket for the specific Hadoop service it intends to access, such as the NameNode service. The TGS grants the requested service ticket, and the Hadoop client caches it.

3.  Accessing the Service (Hadoop Client to Service): With the service ticket in hand, the Hadoop client can now communicate with the target service (e.g., the NameNode). The Hadoop RPC (Remote Procedure Call) mechanism uses this service ticket to reach out to the NameNode. A mutual exchange of tickets occurs between the client and the NameNode. The client's service ticket proves its identity, and the NameNode's ticket confirms its own identity, ensuring that both parties are certain they are communicating with an authenticated entity. This two-way verification is known as mutual authentication.

4.  Authorization: After authentication is complete, the system proceeds to authorization. This is a separate step where the NameNode checks if the authenticated user has the necessary permissions to perform the requested action, such as listing the root directory. If permissions are granted, the NameNode returns the results. The video notes that HDFS authorization (file permissions and ACLs) is covered in a separate video.