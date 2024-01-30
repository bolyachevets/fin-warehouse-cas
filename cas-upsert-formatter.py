import os

insert_cmd = 'INSERT INTO'
values_cmd = 'VALUES'
constraints = {'gl_je_lines': '(je_header_id, je_line_number)',
               'ar_transactions': '(txn_id)',
               'ar_receipts': '(receipt_id)',
               'ar_applied_receivables': '(applied_receivable_key)',
               'ar_adjustments': '(adjustment_number, org_id, adjustment_id)',
               'ap_invoices':  '(invoice_id)'}

skip_files = ['AP_INVOICE_PAYMENTS_output.sql']

def process_update(path, update_file):
    host = open(os.path.join(path, update_file), "r")
    try:
        with open(path + '/' + '_delta.sql', "w") as out:
            out.write('SET client_encoding TO \'UTF8\';\n')
            out.write('SET synchronous_commit TO off;\n')
            out.write('SET search_path TO CAS;\n')
            for line in host:
                if insert_cmd in line:
                    print(line)
                    els = line.split(' ')
                    table_name = els[2]
                    table_cols = els[3]
                    table_vals = line.split(values_cmd, 1)[1]
                    table_vals = table_vals[:-2]
                    table_cols_split = table_cols[1:-1].split(',')
                    table_cols_split_excluded = ['excluded.' + c for c in table_cols_split]
                    cols = '(' + ','.join(table_cols_split_excluded) + ')'
                    command = insert_cmd + ' cas.' + table_name + ' ' + table_cols + ' VALUES ' + table_vals + \
                              ' ON CONFLICT ' + constraints[table_name] + ' DO UPDATE SET ' + table_cols + ' = ' \
                              + cols + ';' + '\n'
                    out.write(command)
    finally:
        host.close()
        os.rename(path + '/' + '_delta.sql', os.path.join(path, update_file))


if __name__ == '__main__':
    update_dir = os.environ['UPDATE_DIR']
    for i in os.listdir(update_dir):
        if os.path.isfile(os.path.join(update_dir, i)) and '_output.sql' in i and i not in skip_files:
            print('starting...')
            print(i)
            process_update(update_dir, i)
            print('processed...')
            print('------------------------------------------')
