import React, { useState, useCallback } from 'react';
import axios from 'axios';
import axios from 'axios';
// Actually the previous code used native events, sticking to native to avoid dep issues
import { Upload, Camera, Loader2, ScanLine, X, FileImage } from 'lucide-react';
import { Button, Card, CardContent } from './ui';
import { ScanResponse } from '../types';

interface UploadPrescriptionProps {
    onScanComplete: (data: ScanResponse) => void;
}

export const UploadPrescription: React.FC<UploadPrescriptionProps> = ({ onScanComplete }) => {
    const [file, setFile] = useState<File | null>(null);
    const [preview, setPreview] = useState<string | null>(null);
    const [isScanning, setIsScanning] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [isDragActive, setIsDragActive] = useState(false);

    const onDrop = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        setIsDragActive(false);
        if (e.dataTransfer.files?.[0]) {
            handleFileSelect(e.dataTransfer.files[0]);
        }
    }, []);

    const onFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files?.[0]) {
            handleFileSelect(e.target.files[0]);
        }
    };

    const handleFileSelect = (selectedFile: File) => {
        setFile(selectedFile);
        const reader = new FileReader();
        reader.onloadend = () => {
            setPreview(reader.result as string);
        };
        reader.readAsDataURL(selectedFile);
        setError(null);
    };

    const clearFile = () => {
        setFile(null);
        setPreview(null);
        setError(null);
    };

    const handleScan = async () => {
        if (!file) return;

        setIsScanning(true);
        setError(null);

        const formData = new FormData();
        formData.append('file', file);

        const apiUrl = import.meta.env.VITE_API_URL || '';
        try {
            const response = await axios.post<ScanResponse>(`${apiUrl}/api/prescriptions/scan`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            onScanComplete(response.data);
        } catch (err: any) {
            console.error("Scan error:", err);
            setError(err.response?.data?.detail || "Failed to analyze prescription. Please ensure the image is clear.");
        } finally {
            setIsScanning(false);
        }
    };

    return (
        <div className="max-w-xl mx-auto mt-10 p-6">
            <h1 className="text-3xl font-bold text-slate-900 mb-2 text-center">Pharmacy Automation</h1>
            <p className="text-slate-500 text-center mb-8">AI-Powered Prescription Analysis</p>

            <Card
                className={`border-2 border-dashed transition-colors overflow-hidden ${isDragActive ? 'border-blue-500 bg-blue-50' : 'border-slate-300'
                    }`}
                onDragOver={(e) => { e.preventDefault(); setIsDragActive(true); }}
                onDragLeave={() => setIsDragActive(false)}
                onDrop={onDrop}
            >
                <CardContent className="flex flex-col items-center justify-center p-8 min-h-[300px]">
                    {isScanning ? (
                        <div className="flex flex-col items-center animate-in fade-in duration-300">
                            <div className="relative">
                                <div className="absolute inset-0 bg-blue-100 rounded-full animate-ping opacity-75"></div>
                                <Loader2 className="relative w-16 h-16 text-blue-600 animate-spin" />
                            </div>
                            <h3 className="text-xl font-semibold text-slate-900 mt-6 mb-2">Analyzing Prescription...</h3>
                            <p className="text-slate-500">Extracting medicine details and dosages</p>
                        </div>
                    ) : !file ? (
                        // Upload State
                        <div className="flex flex-col items-center animate-in fade-in duration-300">
                            <div className="bg-blue-100 p-4 rounded-full mb-4">
                                <Upload className="w-10 h-10 text-blue-600" />
                            </div>
                            <h3 className="text-xl font-semibold text-slate-900 mb-2">Upload Prescription</h3>
                            <p className="text-slate-500 mb-6 text-center max-w-sm">
                                Drag and drop your prescription image here, or click to browse files
                            </p>

                            <div className="flex gap-4">
                                <Button onClick={() => document.getElementById('file-upload')?.click()}>
                                    Choose File
                                </Button>
                                <input
                                    id="file-upload"
                                    type="file"
                                    className="hidden"
                                    accept="image/*,.pdf"
                                    onChange={onFileChange}
                                />
                                <Button variant="outline">
                                    <Camera className="w-4 h-4 mr-2" />
                                    Camera
                                </Button>
                            </div>
                        </div>
                    ) : (
                        // Preview State
                        <div className="w-full animate-in fade-in zoom-in duration-300">
                            <div className="relative rounded-lg overflow-hidden border border-slate-200 shadow-sm bg-slate-50 mb-6 group">
                                <div className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity">
                                    <Button size="icon" variant="destructive" onClick={clearFile} className="h-8 w-8">
                                        <X className="w-4 h-4" />
                                    </Button>
                                </div>
                                {preview ? (
                                    <img src={preview} alt="Preview" className="w-full h-48 object-cover" />
                                ) : (
                                    <div className="h-48 flex items-center justify-center">
                                        <FileImage className="w-12 h-12 text-slate-300" />
                                    </div>
                                )}
                                <div className="p-3 bg-white border-t border-slate-100">
                                    <p className="text-sm font-medium text-slate-700 truncate">{file.name}</p>
                                    <p className="text-xs text-slate-400">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                                </div>
                            </div>

                            <Button
                                onClick={handleScan}
                                size="lg"
                                className="w-full bg-blue-600 hover:bg-blue-700 shadow-lg shadow-blue-200 h-12 text-lg"
                            >
                                <ScanLine className="mr-2 h-5 w-5" />
                                Analyze Prescription
                            </Button>

                            <button
                                onClick={clearFile}
                                className="w-full mt-3 text-sm text-slate-500 hover:text-slate-700"
                            >
                                Cancel and choose another file
                            </button>
                        </div>
                    )}

                    {error && (
                        <div className="mt-6 p-4 bg-red-50 text-red-600 text-sm rounded-lg flex items-center animate-in slide-in-from-bottom-2">
                            <X className="w-4 h-4 mr-2 flex-shrink-0" />
                            {error}
                        </div>
                    )}
                </CardContent>
            </Card>
        </div>
    );
};
