import React, { useState } from 'react';
import axios from 'axios';
import { AlertCircle, CheckCircle, Printer, Loader2 } from 'lucide-react';
import { Button, Card, CardContent, CardHeader, CardTitle, Input } from './ui';
import { ScanResponse } from '../types';
import { cn, formatCurrency } from '../lib/utils';

interface BillReviewProps {
    billData: ScanResponse;
    onReset: () => void;
}

export const BillReview: React.FC<BillReviewProps> = ({ billData, onReset }) => {
    const [pin, setPin] = useState("");
    const [isConfirming, setIsConfirming] = useState(false);
    const [confirmed, setConfirmed] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleConfirm = async () => {
        setIsConfirming(true);
        setError(null);
        try {
            await axios.post(`/api/bills/${billData.bill_id}/confirm`, {
                pharmacist_pin: pin
            });
            setConfirmed(true);
        } catch (err: any) {
            setError(err.response?.data?.detail || "Confirmation failed");
        } finally {
            setIsConfirming(false);
        }
    };

    if (confirmed) {
        return (
            <div className="max-w-2xl mx-auto mt-10 text-center">
                <Card className="bg-green-50 border-green-200">
                    <CardContent className="pt-6">
                        <CheckCircle className="w-16 h-16 text-green-600 mx-auto mb-4" />
                        <h2 className="text-2xl font-bold text-green-800 mb-2">Transaction Complete</h2>
                        <p className="text-green-700 mb-6">Bill confirmed and inventory updated.</p>
                        <div className="flex justify-center gap-4">
                            <Button onClick={() => window.print()} variant="outline" className="bg-white">
                                <Printer className="w-4 h-4 mr-2" /> Print Receipt
                            </Button>
                            <Button onClick={onReset} className="bg-blue-600 hover:bg-blue-700">
                                Process Next Bill
                            </Button>
                        </div>
                    </CardContent>
                </Card>
            </div>
        );
    }

    return (
        <div className="max-w-4xl mx-auto mt-6 p-4">
            <div className="flex justify-between items-center mb-6">
                <div>
                    <h2 className="text-2xl font-bold">Review Bill</h2>
                    <p className="text-slate-500">#{billData.bill_number}</p>
                </div>
                <div className="text-right">
                    <p className="text-sm font-medium">Confidence Score</p>
                    <span className={cn(
                        "inline-block px-2 py-1 rounded text-sm font-bold",
                        billData.extraction_confidence > 0.8 ? "bg-green-100 text-green-800" : "bg-yellow-100 text-yellow-800"
                    )}>
                        {(billData.extraction_confidence * 100).toFixed(0)}%
                    </span>
                </div>
            </div>

            <div className="grid gap-6 md:grid-cols-3">
                <div className="md:col-span-2 space-y-4">
                    {/* Clinical Analysis Card */}
                    {billData.clinical_analysis && (
                        <Card className="bg-blue-50 border-blue-200">
                            <CardHeader className="pb-2">
                                <CardTitle className="text-blue-900 flex items-center gap-2">
                                    <AlertCircle className="w-5 h-5" />
                                    Clinical Review
                                </CardTitle>
                            </CardHeader>
                            <CardContent className="space-y-3">
                                {billData.clinical_analysis.inferred_diagnosis && (
                                    <div>
                                        <h4 className="font-semibold text-blue-900 text-sm">Potential Diagnosis</h4>
                                        <p className="text-blue-800 text-sm">{billData.clinical_analysis.inferred_diagnosis}</p>
                                    </div>
                                )}
                                {billData.clinical_analysis.patient_advice && (
                                    <div>
                                        <h4 className="font-semibold text-blue-900 text-sm">Patient Advice</h4>
                                        <p className="text-blue-800 text-sm">{billData.clinical_analysis.patient_advice}</p>
                                    </div>
                                )}
                                {billData.clinical_analysis.pharmacist_notes && (
                                    <div className="bg-white p-3 rounded border border-blue-100 mt-2">
                                        <h4 className="font-semibold text-slate-900 text-xs uppercase tracking-wide mb-1">Pharmacist Alert</h4>
                                        <p className="text-slate-700 text-sm">{billData.clinical_analysis.pharmacist_notes}</p>
                                    </div>
                                )}
                            </CardContent>
                        </Card>
                    )}

                    <Card>
                        <CardHeader>
                            <CardTitle>Medicines</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="space-y-4">
                                {billData.medicines.map((item, idx) => (
                                    <div key={idx} className={cn(
                                        "flex justify-between items-start p-3 rounded border",
                                        !item.found_in_inventory ? "bg-red-50 border-red-200" :
                                            !item.stock_available ? "bg-yellow-50 border-yellow-200" : "bg-white border-slate-100"
                                    )}>
                                        <div>
                                            <p className="font-medium text-slate-900">{item.generic_name} {item.strength}</p>
                                            <p className="text-sm text-slate-500">{item.frequency || "No frequency"} • {item.duration || "No duration"}</p>
                                            {!item.found_in_inventory && (
                                                <p className="text-xs text-red-600 font-medium mt-1">Not found in inventory</p>
                                            )}
                                            {item.found_in_inventory && !item.stock_available && (
                                                <p className="text-xs text-yellow-600 font-medium mt-1">Low Stock (Available: {item.stock_available ? 'Yes' : 'No'})</p>
                                            )}
                                        </div>
                                        <div className="text-right">
                                            <p className="font-medium">{formatCurrency(item.line_total || 0)}</p>
                                            <p className="text-xs text-slate-500">{item.quantity_prescribed} x {item.unit_price || 0}</p>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </CardContent>
                    </Card>
                </div>

                <div className="space-y-4">
                    <Card>
                        <CardHeader>
                            <CardTitle>Summary</CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-2">
                            <div className="flex justify-between text-sm">
                                <span className="text-slate-500">Subtotal</span>
                                <span>{formatCurrency(billData.subtotal)}</span>
                            </div>
                            <div className="flex justify-between text-sm">
                                <span className="text-slate-500">GST (Total)</span>
                                <span>{formatCurrency(billData.total_gst)}</span>
                            </div>
                            <div className="border-t border-slate-200 my-2 pt-2 flex justify-between font-bold text-lg">
                                <span>Total</span>
                                <span>{formatCurrency(billData.final_amount)}</span>
                            </div>
                        </CardContent>
                    </Card>

                    <Card>
                        <CardHeader>
                            <CardTitle className="text-sm uppercase tracking-wider text-slate-500">Pharmacist Authorization</CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            {error && (
                                <div className="p-2 bg-red-50 text-red-600 text-sm rounded flex items-center">
                                    <AlertCircle className="w-4 h-4 mr-2" />
                                    {error}
                                </div>
                            )}
                            <div>
                                <label className="text-xs font-medium text-slate-700 block mb-1">Enter PIN to Confirm</label>
                                <Input
                                    type="password"
                                    value={pin}
                                    onChange={(e) => setPin(e.target.value)}
                                    placeholder="Enter PIN (e.g. 1234)"
                                    className="text-center tracking-widest"
                                />
                            </div>
                            <div className="grid grid-cols-2 gap-2">
                                <Button variant="outline" onClick={onReset}>Reject</Button>
                                <Button
                                    onClick={handleConfirm}
                                    disabled={!pin || isConfirming}
                                    className="bg-blue-600 hover:bg-blue-700"
                                >
                                    {isConfirming ? <Loader2 className="animate-spin w-4 h-4" /> : "Confirm Bill"}
                                </Button>
                            </div>
                        </CardContent>
                    </Card>
                </div>
            </div>
        </div>
    );
};
