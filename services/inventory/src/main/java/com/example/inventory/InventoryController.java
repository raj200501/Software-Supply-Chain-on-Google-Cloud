package com.example.inventory;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/inventory")
public class InventoryController {
    private final Map<String, InventoryItem> items = new ConcurrentHashMap<>();

    public InventoryController() {
        items.put("item-1", new InventoryItem("item-1", "SKU-1", "Sample Item", 10));
    }

    @GetMapping("/{id}")
    public ResponseEntity<InventoryItem> getItem(@PathVariable String id) {
        InventoryItem item = items.get(id);
        if (item == null) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(item);
    }

    @PostMapping("/reserve")
    public ResponseEntity<InventoryItem> reserve(@RequestBody ReserveRequest request) {
        InventoryItem item = items.get(request.itemId());
        if (item == null) {
            return ResponseEntity.notFound().build();
        }
        if (item.quantity() < request.quantity()) {
            return ResponseEntity.status(409).build();
        }
        InventoryItem updated = new InventoryItem(item.id(), item.sku(), item.name(), item.quantity() - request.quantity());
        items.put(updated.id(), updated);
        return ResponseEntity.ok(updated);
    }

    public record InventoryItem(String id, String sku, String name, int quantity) {}

    public record ReserveRequest(String itemId, int quantity) {}
}
