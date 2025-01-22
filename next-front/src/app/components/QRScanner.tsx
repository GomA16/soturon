"use client";
import QrScanner from 'qr-scanner';
import { FC, useEffect, useRef, useState } from 'react';

type Props = {
  onDecode?: (result: string) => void;
  loading?: React.ReactNode;
};

const QRScanner: FC<Props> = ({
  onDecode = (result) => console.log("Scanned QR Code Content:", result),
  loading = <p>Loading camera...</p>,
}) => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const qrScannerRef = useRef<QrScanner | null>(null);
  const [isBooting, setIsBooting] = useState(true);

  useEffect(() => {
    if (videoRef.current) {
      qrScannerRef.current = new QrScanner(
        videoRef.current,
        (result) => {
          onDecode(result.data);
        },
        {
          returnDetailedScanResult: true,
          highlightScanRegion: true,
          highlightCodeOutline: true,
        },
      );
      qrScannerRef.current.start().then(() => {
        setIsBooting(false); //
      });
    }
    return () => {
      if (qrScannerRef.current) {
        qrScannerRef.current.destroy(); 
      }
    };
  }, [onDecode]);

  return (
    <>
      {isBooting && loading}
      <video ref={videoRef} style={{ width: '100%', maxHeight: '50vh' }} />
    </>
  );
};

export default QRScanner;