import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import { Pill } from 'lucide-react';
import { UploadPrescription } from './components/UploadPrescription';
import { BillReview } from './components/BillReview';
import { InventoryDashboard } from './components/InventoryDashboard';
import { LandingPage } from './pages/LandingPage';
import { ScanResponse } from './types';

function MainApp() {
    const [activeBill, setActiveBill] = useState<ScanResponse | null>(null);

    const handleScanComplete = (data: ScanResponse) => {
        setActiveBill(data);
    };

    return activeBill ? (
        <BillReview billData={activeBill} onReset={() => setActiveBill(null)} />
    ) : (
        <UploadPrescription onScanComplete={handleScanComplete} />
    );
}

function AppContent() {
    const location = useLocation();
    const isLanding = location.pathname === '/';

    return (
        <div className="min-h-screen bg-slate-50 font-sans text-slate-900">
            {/* Navigation - Hide on Landing Page */}
            {!isLanding && (
                <nav className="bg-white border-b border-slate-200 sticky top-0 z-50">
                    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                        <div className="flex justify-between h-16">
                            <div className="flex">
                                <Link to="/" className="flex-shrink-0 flex items-center gap-2">
                                    <div className="bg-blue-600 p-1.5 rounded-lg text-white">
                                        <Pill className="h-6 w-6" />
                                    </div>
                                    <span className="font-bold text-xl tracking-tight text-slate-900">MedEase</span>
                                </Link>
                                <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                                    <Link to="/app" className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${location.pathname === '/app' ? 'border-blue-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'}`}>
                                        New Bill
                                    </Link>
                                    <Link to="/inventory" className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${location.pathname === '/inventory' ? 'border-blue-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'}`}>
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
            )}

            {/* Main Content */}
            <main className={!isLanding ? "py-10" : ""}>
                <Routes>
                    <Route path="/" element={<LandingPage />} />
                    <Route path="/app" element={<MainApp />} />
                    <Route path="/inventory" element={<InventoryDashboard />} />
                </Routes>
            </main>
        </div>
    );
}

function App() {
    return (
        <Router>
            <AppContent />
        </Router>
    );
}

export default App;
