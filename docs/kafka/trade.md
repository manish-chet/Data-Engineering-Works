## **The Scenario: Leader Broker Failure and Data Loss Risk**

Consider a situation where you have a topic partition `P2` with replicas on `Broker 1`, `Broker 2`, and `Broker 3`. Suppose `Broker 3` holds the leader for `P2`, and `Broker 1` and `Broker 2` hold its followers. Initially, all three are in-sync (ISR: 3, 2, 1).

**New Leader Election**

If the leader broker (`Broker 3`) goes down, a new leader must be chosen from the remaining in-sync replicas. For example, `Broker 2` might be elected as the new leader. At this point, the ISR would only include the active, in-sync replicas (e.g., ISR: 2, 1), as the original leader's broker is down.

**The Critical Data Loss Scenario**

Now, let's say the new leader (`Broker 2`) receives `Message 3` from a producer, but before `Message 3` can be fully replicated to the remaining follower (`Broker 1`), `Broker 2` also goes down.

At this point:

  `Message 3` was written to `Broker 2`'s partition.
  `Broker 2` is now down, making `Message 3` inaccessible via its original location.
  `Broker 1` is still up, but it only has `Message 1` and `Message 2`, not `Message 3` because replication was incomplete.

Result: There is currently no in-sync replica that holds all the latest data, including `Message 3`. This is where the trade-off comes in.

## **The Trade-Off: Availability vs. Durability**

When there are no in-sync replicas available for a partition, Kafka faces a critical decision:

**Option 1**: Prioritize Durability (No Data Loss)

  Action: The partition `P2` becomes unavailable, and producers cannot publish new messages to it.
  
  Outcome: Data loss is prevented because the system waits for the original leader or a lagging replica to come back online and fully synchronize before accepting new writes.
  
  System State: The system is highly durable (reliable) but potentially less available.

**Option 2**: Prioritize Availability (Potential Data Loss)
   
  Action: A partition that is not fully in-sync (e.g., `Broker 1`'s partition `P2`, which is missing `Message 3`) is chosen as the new leader. Producers can then immediately start publishing new messages (`Message 4`, `Message 5`, etc.) to this new leader.
  
  Outcome: `Message 3` is permanently lost because it was only present on the now-down `Broker 2` and never fully replicated to `Broker 1`.
  
  System State: The system is highly available (continuous operation) but potentially less durable due to data loss.

This choice is controlled by a Kafka configuration property: `unclean.leader.election.enable`.

## **unclean.leader.election.enable Configuration**

This crucial Kafka property determines which of the two options (durability or availability) Kafka will prioritize during a leader failure when no in-sync replicas are available.

1. unclean.leader.election.enable = true
    
Behavior: Allows Kafka to elect a replica that is not in-sync (i.e., it's "unclean" because it doesn't have all the latest data) as the new leader.
    
Benefit: Keeps the system highly available. Producers can continue writing immediately.
    
Risk: There might be some amount of data loss (as seen with `Message 3` in our example).
    
Use Cases: Suitable for scenarios where a small amount of data loss is acceptable, such as:
    Log aggregation
    Metrics calculation

2. unclean.leader.election.enable = false
    
Behavior: Prevents a replica that is not in-sync from becoming the leader. The system will wait until an in-sync replica becomes available or the original leader recovers and synchronizes.
      
Benefit: Ensures the system is highly durable, meaning no data will be lost.
    
Risk: The partition will be unavailable for a period, blocking producers from publishing messages until an in-sync leader is established.
    
Use Cases: Essential for scenarios where data loss is absolutely unacceptable, such as:
    Transaction-related information in banking or financial sectors
    Any system where monetary transactions are involved

