// session-06_restock.js · run with:  mongosh kgs session-06_restock.js
// or inside mongosh:                 load("session-06_restock.js")
const LOW = 5;                                   // JavaScript variable
const today = new Date();

print(`Low-stock report for ${db.getName()} on ${today.toISOString().slice(0, 10)}`);

const low = db.products.find({ stock: { $lt: LOW } }, { name: 1, stock: 1 }).sort({ stock: 1 });
low.forEach(p => {
  const order = LOW * 2 - p.stock;              // bring stock up to 10
  print(`  ${p.name.padEnd(28)} stock ${String(p.stock).padStart(2)} -> reorder ${order}`);
  db.reorders.insertOne({ productId: p._id, qty: order, createdAt: today });
});

printjson(db.reorders.aggregate([{ $group: { _id: null, lines: { $sum: 1 }, units: { $sum: "$qty" } } }]).toArray());
