import { Link } from "react-router-dom";

export default function NewsCard({ news }) {
  const date = news.published_at
    ? new Date(news.published_at).toLocaleDateString("tr-TR")
    : new Date(news.fetched_at).toLocaleDateString("tr-TR");

  return (
    <div style={{ border: "1px solid #ddd", borderRadius: 8, padding: 16, marginBottom: 12 }}>
      <div style={{ fontSize: 12, color: "#888", marginBottom: 4 }}>
        {news.source} {news.category && `• ${news.category}`} • {date}
      </div>
      <Link to={`/news/${news.id}`} style={{ textDecoration: "none", color: "inherit" }}>
        <h3 style={{ margin: "0 0 8px" }}>{news.title}</h3>
      </Link>
      {news.summary && <p style={{ margin: 0, color: "#555", fontSize: 14 }}>{news.summary}</p>}
    </div>
  );
}
