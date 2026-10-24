# Session 8 · A replica set in miniature: oplog, write concern and failover
# This is a teaching model (no real servers): it mimics how a 3-member replica set behaves.

class Member:
    def __init__(self, name, priority=1):
        self.name, self.priority, self.up = name, priority, True
        self.data, self.oplog = {}, []          # oplog = ordered list of operations applied

    def apply(self, op):
        self.oplog.append(op)
        kind, key, val = op
        if kind == "set": self.data[key] = val
        elif kind == "del": self.data.pop(key, None)

class ReplicaSet:
    def __init__(self, members):
        self.members = members
        self.primary = max(members, key=lambda m: m.priority)
        print(f"rs.initiate(): {self.primary.name} elected PRIMARY")

    def write(self, key, val, w=1):
        if not self.primary or not self.primary.up:
            raise RuntimeError("NotWritablePrimary: no primary available")
        op = ("set", key, val)
        self.primary.apply(op)
        acks = 1
        for m in self.members:                   # secondaries tail the primary's oplog
            if m is not self.primary and m.up:
                m.apply(op); acks += 1
        needed = len(self.members) // 2 + 1 if w == "majority" else w
        status = "acknowledged" if acks >= needed else "WriteConcernError (waiting for replication)"
        print(f"  write {key}={val!r:<10} w={w!s:<8} acks={acks}/{len(self.members)} -> {status}")

    def elect(self):
        alive = [m for m in self.members if m.up]
        if len(alive) <= len(self.members) // 2:
            self.primary = None
            print(f"  election FAILED: only {len(alive)} of {len(self.members)} members up (no majority) -> read-only")
            return
        # the most up-to-date member with the highest priority wins
        self.primary = max(alive, key=lambda m: (len(m.oplog), m.priority))
        print(f"  election: {self.primary.name} is the new PRIMARY")

    def status(self):
        for m in self.members:
            role = "PRIMARY" if m is self.primary else ("SECONDARY" if m.up else "DOWN")
            print(f"    {m.name:<6} {role:<9} oplog={len(m.oplog)} data={m.data}")

rs = ReplicaSet([Member("node1", priority=2), Member("node2"), Member("node3")])
rs.write("stock:101", 40)
rs.write("stock:102", 15, w="majority")
rs.status()

print("\nnode1 crashes")
rs.members[0].up = False
rs.elect()
rs.write("stock:101", 39, w="majority")
rs.status()

print("\nnode3 also goes down")
rs.members[2].up = False
rs.write("stock:103", 6, w=1)
rs.write("stock:104", 0, w="majority")
rs.elect()
try:
    rs.write("stock:105", 9)
except RuntimeError as e:
    print("  ", e)
