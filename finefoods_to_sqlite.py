import gzip
import sqlite3
import itertools

dbcon = sqlite3.connect( "finefoods.db" )
cursor = dbcon.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS review (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  productid VARCHAR,
  reviewerid VARCHAR,
  reviewername VARCHAR,
  reviewhelpful VARCHAR,
  reviewscore INTEGER,
  reviewtime INTEGER,
  reviewsummary VARCHAR,
  reviewtext VARCHAR
);
""")

FIELDS = ('product/productId',
          'review/userId',
          'review/profileName',
          'review/helpfulness',
          'review/score',
          'review/time',
          'review/summary',
          'review/text')
FIELDS_SET = set(FIELDS)

def entry_iter():
    with gzip.open("finefoods.txt.gz", "rt", encoding="Latin1") as fh_in:
        line_i = 0
        d = dict()
        current_value = None
        while True:
            try:
                line = next(fh_in)
            except StopIteration:
                # end of file reached
                break
            if line == '\n':
                d[current_field] = ''.join(current_value).rstrip()
                d['review/time'] = int(d['review/time'])
                d['review/score'] = int(float(d['review/score']))
                yield(tuple(d[x] for x in FIELDS))
                d = dict()
                review_text = None
            else:
                i = line.find(': ')
                if i == -1:
                    current_value.append(line)
                else:
                    field = line[:i]
                    if field in FIELDS_SET:
                        if current_value is not None:
                            d[current_field] = ''.join(current_value).rstrip()
                        current_field = field
                        current_value = [line[(i+2):]]
                    else:
                        current_value.append(value)                    

sql = '''
INSERT INTO review (
  productid,
  reviewerid,
  reviewername,
  reviewhelpful,
  reviewscore,
  reviewtime,
  reviewsummary,
  reviewtext
) VALUES (
  ?,
  ?,
  ?,
  ?,
  ?,
  ?,
  ?,
  ?
)'''


it = entry_iter()
BATCH_SIZE = 25000
progress = 0
print('\r{:,} entries processed.'.format(progress), end='', flush=True)
while True:
    it_slice = itertools.islice(it, BATCH_SIZE)
    tpl = tuple(it_slice)
    if len(tpl) == 0:
        break
    cursor.executemany(sql, tpl)
    progress += len(tpl)
    print('\r{:,} entries processed.'.format(progress), end='', flush=True)
print()
dbcon.commit()
