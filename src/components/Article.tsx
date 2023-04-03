import React, {useEffect, useState} from "react";
import {useParams} from "react-router-dom";
import ReactMarkdown from "react-markdown";
import {InlineMath, BlockMath} from "react-katex";
import "katex/dist/katex.min.css";
import gfm from "remark-gfm";
import "./Article.css";


interface ArticleProps {
  filePath: string;
}

const Article: React.FC<ArticleProps> = ({ filePath }) => {
  const [content, setContent] = useState("");
  const { id } = useParams<{id: string}>();

  useEffect(() => {
    fetch(`${filePath}/${id}.md`)
      .then((response) => {
        if (!response.ok) {
	  throw new Error("Failed to fetch the article");
	}
	return response.text();
      })
      .then((text) => setContent(text))
      .catch((error) => console.error(error));
  }, [id, filePath]);

  const renderers = {
    inlineMath: ({value}: { value: string }) => <InlineMath math={value} />,
    math: ({value}: {value: string}) => <BlockMath math={value} />,
  };

  return (
    <div className="Article">
      <ReactMarkdown
        children={content}
	components={renderers}
	remarkPlugins={[gfm]}
      />
    </div>
  );
};

export default Article;
