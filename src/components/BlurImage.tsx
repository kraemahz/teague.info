import React, { useState, useRef, useEffect } from "react";
import "./BlurImage.css";

interface BlurImageProps {
  src: string;
  thumbSrc: string;
  alt?: string;
  className?: string;
}

const BlurImage: React.FC<BlurImageProps> = ({ src, thumbSrc, alt = "", className = "" }) => {
  const [loaded, setLoaded] = useState(false);
  const imgRef = useRef<HTMLImageElement>(null);

  useEffect(() => {
    // Handle case where image is already cached
    if (imgRef.current?.complete) {
      setLoaded(true);
    }
  }, []);

  return (
    <div className={`blur-image-wrapper ${className}`}>
      <img
        src={thumbSrc}
        alt=""
        aria-hidden="true"
        className={`blur-image-thumb ${loaded ? "blur-image-hidden" : ""}`}
      />
      <img
        ref={imgRef}
        src={src}
        alt={alt}
        className={`blur-image-full ${loaded ? "blur-image-visible" : ""}`}
        onLoad={() => setLoaded(true)}
      />
    </div>
  );
};

export default BlurImage;
