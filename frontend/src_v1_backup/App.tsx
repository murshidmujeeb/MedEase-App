import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Pill, FileText, BarChart3 } from 'lucide-react';
import { UploadPrescription } from './components/UploadPrescription';
import { BillReview } from './components/BillReview';
import { InventoryDashboard } from './components/InventoryDashboard';
import { ScanResponse } from './types';

function App() {
    const [activeBill, setActiveBill] = useState<ScanResponse | null>(null);

    const handleScanComplete = (data: ScanResponse) => {
        setActiveBill(data);
    };

    return (
        <Router>
            <div className="min-h-screen bg-slate-50 font-sans text-slate-900">
                {/* Navigation */}
                <nav className="bg-white border-b border-slate-200 sticky top-0 z-50">
                    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                        <div className="flex justify-between h-16">
                            <div className="flex">
                                <div className="flex-shrink-0 flex items-center gap-2">
                                    <div className="bg-blue-600 p-1.5 rounded-lg text-white">
                                        <Pill className="h-6 w-6" />
                                    </div>
                                    <span className="font-bold text-xl tracking-tight text-slate-900">MedEase</span>
                                </div>
                                <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                                    <Link to="/" className="border-blue-500 text-gray-900 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
                                        New Bill
                                    </Link>
                                    <Link to="/inventory" className="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
                                        Inventory
                                    </Link>
                                </div>
                            </div>
                            <div className="flex items-center">
                                <div className="flex-shrink-0">
                                    <span className="text-sm text-slate-500 mr-2">Pharmacist ID:</span>
                                    <span className="text-sm font-bold bg-slate-100 px-2 py-1 rounded">ADMIN</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </nav>

                {/* Main Content */}
                <main className="py-10">
                    <Routes>
                        <Route path="/" element={
                            activeBill ? (
                                <BillReview billData={activeBill} onReset={() => setActiveBill(null)} />
                            ) : (
                                <UploadPrescription onScanComplete={handleScanComplete} />
                            )
                        } />
                        <Route path="/inventory" element={<InventoryDashboard />} />
                    </Routes>
                </main>
            </div>
        </Router>
    );
}

export default App;
