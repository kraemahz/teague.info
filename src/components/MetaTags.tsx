import React from 'react';
import { Helmet } from 'react-helmet';

interface ArticleMeta {
  id: string;
  title: string;
  excerpt: string;
  image: string;
}

interface MetaTagsProps {
  article: ArticleMeta;
}

const MetaTags: React.FC<MetaTagsProps> = ({ article }) => {
  const imageUrl = `/images/${article.image}`;
  const title = article.title;
  const description = article.excerpt;

  return (
    <Helmet>
      {/* Open Graph Protocol */}
      <meta property="og:title" content={title} />
      <meta property="og:description" content={description} />
      <meta property="og:image" content={imageUrl} />
      <meta property="og:type" content="website" />

      {/* Twitter Card */}
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:title" content={title} />
      <meta name="twitter:description" content={description} />
      <meta name="twitter:image" content={imageUrl} />
    </Helmet>
  );
};

export default MetaTags;
