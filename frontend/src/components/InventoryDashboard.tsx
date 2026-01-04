import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Search } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent, Input } from './ui';
import { Medicine } from '../types';

export const InventoryDashboard: React.FC = () => {
    const [medicines, setMedicines] = useState<Medicine[]>([]);
    const [search, setSearch] = useState("");
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchInventory = async () => {
            try {
                const apiUrl = import.meta.env.VITE_API_URL || '';
                const response = await axios.get(`${apiUrl}/api/inventory`, {
                    params: { search }
                });
                setMedicines(response.data.medicines);
            } catch (err) {
                console.error(err);
            } finally {
                setLoading(false);
            }
        };

        const timeout = setTimeout(fetchInventory, 300); // Debounce
        return () => clearTimeout(timeout);
    }, [search]);

    return (
        <div className="max-w-6xl mx-auto mt-6 p-4">
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-2xl font-bold text-slate-900">Inventory Management</h1>
                <div className="relative w-72">
                    <Search className="absolute left-3 top-2.5 h-4 w-4 text-slate-400" />
                    <Input
                        placeholder="Search medicines..."
                        className="pl-9"
                        value={search}
                        onChange={(e) => setSearch(e.target.value)}
                    />
                </div>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Current Stock Levels</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="overflow-x-auto">
                        <table className="w-full text-sm text-left">
                            <thead className="bg-slate-50 text-slate-500 uppercase text-xs font-semibold">
                                <tr>
                                    <th className="px-4 py-3">Medicine Name</th>
                                    <th className="px-4 py-3">Type</th>
                                    <th className="px-4 py-3 text-right">Unit Price</th>
                                    <th className="px-4 py-3 text-center">Stock Level</th>
                                    <th className="px-4 py-3 text-center">Status</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-slate-100">
                                {loading ? (
                                    <tr><td colSpan={5} className="text-center py-4">Loading...</td></tr>
                                ) : medicines.map((med) => (
                                    <tr key={med.id} className="hover:bg-slate-50/50">
                                        <td className="px-4 py-3 font-medium text-slate-900">
                                            {med.generic_name} ({med.strength})
                                            {med.brand_names && med.brand_names.length > 0 &&
                                                <span className="block text-xs text-slate-500 font-normal">{med.brand_names.join(", ")}</span>
                                            }
                                        </td>
                                        <td className="px-4 py-3 text-slate-500">{med.form}</td>
                                        <td className="px-4 py-3 text-right">₹{med.unit_price}</td>
                                        <td className="px-4 py-3 text-center font-mono">{med.current_stock}</td>
                                        <td className="px-4 py-3 text-center">
                                            <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${med.stock_status === 'LOW'
                                                ? 'bg-red-100 text-red-700'
                                                : 'bg-green-100 text-green-700'
                                                }`}>
                                                {med.stock_status === 'LOW' ? '⚠️ Low Stock' : 'In Stock'}
                                            </span>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                        {medicines.length === 0 && !loading && (
                            <div className="text-center py-8 text-slate-500">No medicines found.</div>
                        )}
                    </div>
                </CardContent>
            </Card>
        </div>
    );
};
