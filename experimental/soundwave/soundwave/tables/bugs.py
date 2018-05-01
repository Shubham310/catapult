# Copyright 2018 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import pandas  # pylint: disable=import-error


COLUMNS = (
    'id',  # int: crbug number identifying this issue
    'summary',  # string: issue title ('1%-5% regression in loading.mobile ...')
    'published',  # np.datetime64: when the issue got created
    'updated',  # np.datetime64: when the issue got last updated
    'state',  # string: usually either 'open' or 'closed'
    'status',  # string: current state of the bug ('Assigned', 'Fixed', etc.)
    'author',  # string: email of user who created the issue
    'owner',  # string: email of user who currently owns the issue
    'cc',  # string: comma-separated list of users cc'ed into the issue
    'components',  # string: comma-separated list of components ('Blink>Loader')
    'labels',  # string: comma-separated list of labels ('Type-Bug-Regression')
)
INDEX = COLUMNS[0]


def _CommaSeparate(values):
  assert isinstance(values, list)
  if values:
    return ','.join(values)
  else:
    return None


def DataFrameFromJson(data):
  rows = []
  for row in data:
    row = row['bug'].copy()
    for key in ('cc', 'components', 'labels'):
      row[key] = _CommaSeparate(row[key])
    rows.append(tuple(row[k] for k in COLUMNS))

  df = pandas.DataFrame.from_records(rows, index=INDEX, columns=COLUMNS)
  for key in ('published', 'updated'):
    df[key] = pandas.to_datetime(df[key])
  return df
