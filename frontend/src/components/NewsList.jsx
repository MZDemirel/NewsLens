import NewsCard from "./NewsCard";

export default function NewsList({ items }) {
  if (!items || items.length === 0) {
    return <p>Gösterilecek haber yok.</p>;
  }
  return (
    <div>
      {items.map((news) => (
        <NewsCard key={news.id} news={news} />
      ))}
    </div>
  );
}
