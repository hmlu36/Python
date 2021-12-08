
	select StockInfo.stockId        '證券代號',
		   name                     '證券名稱',
		   industry                 '產業別',
		   yearSeason               '年/季',
		   revenue                  '營收(億)',
		   profitAfterTax           '稅後淨利(億)',
		   grossMargin              '毛利(%)',
		   operatingIncome          '營業利益(%)',
		   profitAfterTaxPercentage '稅後淨利(%)',
		   roe                      'ROE(%)',
		   eps                      'EPS(%)',
		   cashDividends            '現金',
		   stockDividends           '股票',
		   totalDividends           '合計股利'
	  from StockInfo
	  join StockDetail
		on StockInfo.stockId = StockDetail.stockId
 left join StockDividend
		on StockInfo.stockId = StockDividend.stockId
	   and StockDividend.year = (select max(year) from StockDividend temp where StockDividend.stockId = temp.stockId)
	 where yearSeason in ('2020', '20Q3')
	 order by StockInfo.stockId;
	   
	   