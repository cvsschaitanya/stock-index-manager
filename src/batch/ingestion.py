from dispatch.DatabaseDispatcher import DatabaseDispatcher
from extract.alphaVantage.AlphaVantageExtractor import AlphaVantageExtractor


def main():
    extractor = AlphaVantageExtractor()
    dispatcher = DatabaseDispatcher("stocks.db", "stocks", "Stock")

    extractor.add_listener(dispatcher)

    extractor.start()

if __name__ == "__main__":
    main()