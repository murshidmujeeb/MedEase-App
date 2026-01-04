import React, { useState } from 'react';
import axios from 'axios';
import { Upload, Camera, Loader2 } from 'lucide-react';
import { Button, Card, CardContent } from './ui';
import { ScanResponse } from '../types';

interface UploadPrescriptionProps {
    onScanComplete: (data: ScanResponse) => void;
}

export const UploadPrescription: React.FC<UploadPrescriptionProps> = ({ onScanComplete }) => {
    const [isDragging, setIsDragging] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleUpload = async (file: File) => {
        setIsLoading(true);
        setError(null);

        try {
            const formData = new FormData();
            formData.append('file', file);

            const response = await axios.post('/api/prescriptions/scan', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });

            onScanComplete(response.data);
        } catch (err) {
            console.error(err);
            setError("Failed to process prescription. Please try again.");
        } finally {
            setIsLoading(false);
        }
    };

    const onDrop = (e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(false);
        if (e.dataTransfer.files?.[0]) {
            handleUpload(e.dataTransfer.files[0]);
        }
    };

    const onFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files?.[0]) {
            handleUpload(e.target.files[0]);
        }
    };

    return (
        <div className="max-w-xl mx-auto mt-10 p-6">
            <h1 className="text-3xl font-bold text-slate-900 mb-8 text-center">Pharmacy Automation</h1>

            <Card
                className={`border-2 border-dashed transition-colors ${isDragging ? 'border-blue-500 bg-blue-50' : 'border-slate-300'
                    }`}
                onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
                onDragLeave={() => setIsDragging(false)}
                onDrop={onDrop}
            >
                <CardContent className="flex flex-col items-center justify-center p-12 text-center h-64">
                    {isLoading ? (
                        <div className="flex flex-col items-center">
                            <Loader2 className="w-12 h-12 text-blue-600 animate-spin mb-4" />
                            <p className="text-lg font-medium text-slate-700">Analyzing Prescription...</p>
                            <p className="text-sm text-slate-500 mt-2">Extracting medicines via Gemini AI</p>
                        </div>
                    ) : (
                        <>
                            <div className="bg-blue-100 p-4 rounded-full mb-4">
                                <Upload className="w-8 h-8 text-blue-600" />
                            </div>
                            <h3 className="text-xl font-semibold text-slate-900 mb-2">Upload Prescription</h3>
                            <p className="text-slate-500 mb-6">Drag and drop file here, or click to browse</p>

                            <div className="flex gap-4">
                                <Button onClick={() => document.getElementById('file-upload')?.click()}>
                                    Choose File
                                </Button>
                                <input
                                    id="file-upload"
                                    type="file"
                                    className="hidden"
                                    accept="image/*,.pdf"
                                    onChange={onFileSelect}
                                />
                                <Button variant="outline">
                                    <Camera className="w-4 h-4 mr-2" />
                                    Camera
                                </Button>
                            </div>
                        </>
                    )}
                    {error && <p className="text-red-500 mt-4">{error}</p>}
                </CardContent>
            </Card>
        </div>
    );
};
