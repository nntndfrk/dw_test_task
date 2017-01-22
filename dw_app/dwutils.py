# -*- coding: utf-8 -*-
import json
import datetime
import pandas as pd
import numpy as np

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)




class MainData:
    def __init__(self, dw, categories, shops, date1, date2):
        self.dw = dw
        self.categories = categories
        self.shops = shops
        self.date1 = date1
        self.date2 = date2


    @staticmethod
    def get_rec_df(dw, categories, shops, date):
        receipts_data = dw.get_receipts(
            categories=categories,
            shops=shops,
            date_from=date,
            date_to=date,
            type="short")
        t = []  # шото придумать
        i = []
        for item in receipts_data:
            t.append(item['turnover'])
            i.append(item['receipt_id'])
        return pd.DataFrame(t, index=i)


    @staticmethod
    def get_categ_df(dw, categories, shops, date):
        # categories.append('sum')
        categ_df = dw.get_categories_sale(
            categories=categories,
            shops=shops,
            date_from=date,
            date_to=date,
            by=['turnover', 'qty', 'receipts_qty'],
            view_type='raw')
        return categ_df


    @property
    def get_main_data(self):
        data = dict()
        categ_df1 = MainData.get_categ_df(dw=self.dw,
                                          categories=self.categories[:],
                                          shops=self.shops,
                                          date=self.date1)
        rec_df1 = MainData.get_rec_df(dw=self.dw,
                                      categories=self.categories,
                                      shops=self.shops,
                                      date=self.date1)

        categ_df2 = MainData.get_categ_df(dw=self.dw,
                                          categories=self.categories[:],
                                          shops=self.shops,
                                          date=self.date2)
        rec_df2 = MainData.get_rec_df(dw=self.dw,
                                      categories=self.categories,
                                      shops=self.shops,
                                      date=self.date2)

        def get_data(categ_df, rec_df):

            data = dict()

            try:
                data['turnover'] = categ_df['turnover'].sum()
            except:
                data['turnover'] = None
            try:
                data['qty'] = categ_df['qty'].sum()#???
            except:
                data['qty'] = None
            try:
                data['receipts_qty'] = categ_df['receipts_qty'].sum()
            except:
                data['receipts_qty'] = None
            try:
                data['receipts_mean'] = round(np.asscalar(rec_df.mean()), 2)
            except:
                data['receipts_mean'] = None

            return data

        data['date1'] = get_data(categ_df1, rec_df1)
        data['date1']['date'] = self.date1.strftime('%d-%m-%Y')
        data['date2'] = get_data(categ_df2, rec_df2)
        data['date2']['date'] = self.date2.strftime('%d-%m-%Y')
        try:
            data['turnover_diff'] = data['date1']['turnover'] - data['date2']['turnover']
        except (ValueError, ZeroDivisionError, TypeError):
            data['turnover_diff'] = None
        try:
            data['receipts_qty_diff'] = data['date1']['receipts_qty'] - data['date2']['receipts_qty']
        except (ValueError, ZeroDivisionError, TypeError):
            data['receipts_qty_diff'] = None
        # import pdb
        # pdb.set_trace()
        try:
            data['qty_diff'] = data['date1']['qty'] - data['date2']['qty']
        except (ValueError, ZeroDivisionError, TypeError):
            data['qty_diff'] = None
        try:
            data['receipts_mean_diff'] = data['date1']['receipts_mean'] - data['date2']['receipts_mean']
        except (ValueError, ZeroDivisionError, TypeError):
            data['receipts_mean_diff'] = None
        try:
            data['turnover_diff_perc'] = ((data['date1']['turnover'] - data['date2']['turnover'])/abs(data['date2']['turnover']))*100
        except (ValueError, ZeroDivisionError, TypeError):
            data['turnover_diff_perc'] = None
        try:
            data['receipts_qty_diff_perc'] = (float(data['receipts_qty_diff'])/abs(data['date2']['receipts_qty']))*100
        except (ValueError, ZeroDivisionError, TypeError):
            data['receipts_qty_diff_perc'] = None
        try:
            data['qty_diff_perc'] = (float(data['qty_diff'])/abs(data['date2']['qty']))*100
        except (ValueError, ZeroDivisionError, TypeError):
            data['qty_diff_perc'] = None
        try:
            data['receipts_mean_diff_perc'] = ((data['date1']['receipts_mean'] - data['date2']['receipts_mean'])/abs(data['date2']['receipts_mean']))*100
        except (ValueError, ZeroDivisionError, TypeError):
            data['receipts_mean_diff_perc'] = None
        
        return data


class ProductsData:
    def __init__(self, dw, categories, shops, date1, date2):
        self.dw = dw
        self.categories = categories
        self.shops = shops
        self.date1 = date1
        self.date2 = date2

    @staticmethod
    def get_prod_turn(dw, categories, shops, date):
        prod_turn_data = dw.get_products_sale(
                categories=categories,
                shops = shops,
                by = 'turnover',
                date_from = date,
                date_to = date,
                show = 'name',
                view_type = "represent")
        return prod_turn_data.T

    @staticmethod
    def get_prod_qt(dw, categories, shops, date):
        prod_qt_data = dw.get_products_sale(
            categories=categories,
            shops=shops,
            by='qty',
            date_from=date,
            date_to=date,
            show='name',
            view_type="represent")
        return prod_qt_data.T

    @property
    def get_prod_data(self):
        prod_turn1 = ProductsData.get_prod_turn(dw=self.dw,
                                                categories=self.categories,
                                                shops=self.shops,
                                                date=self.date1)
        prod_turn2 = ProductsData.get_prod_turn(dw=self.dw,
                                                categories=self.categories,
                                                shops=self.shops,
                                                date=self.date2)
        prod_qty1 = ProductsData.get_prod_qt(dw=self.dw,
                                             categories=self.categories,
                                             shops=self.shops,
                                             date=self.date1)
        prod_qty2 = ProductsData.get_prod_qt(dw=self.dw,
                                             categories=self.categories,
                                             shops=self.shops,
                                             date=self.date2)

        data1 = pd.concat([prod_turn1, prod_turn2], axis=1)
        data1.fillna(value=0, axis=1, inplace=True)
        try:
            data1['turn_diff'] = data1[self.date1.strftime('%Y-%m-%d')]-data1[self.date2.strftime('%Y-%m-%d')]
        except:
            data1['turn_diff'] = None
        try:
            data1.drop([self.date1.strftime('%Y-%m-%d'), self.date2.strftime('%Y-%m-%d')], axis=1, inplace=True)
        except:
            pass
        data2 = pd.concat([prod_qty1, prod_qty2], axis=1)
        data2.fillna(value=0, axis=1, inplace=True)
        try:
            data2['qty_diff'] = data2[self.date1.strftime('%Y-%m-%d')] - data2[self.date2.strftime('%Y-%m-%d')]
        except:
            data2['qty_diff'] = None
        try:
            data2.drop([self.date1.strftime('%Y-%m-%d'), self.date2.strftime('%Y-%m-%d')], axis=1, inplace=True)
        except:
            pass
        data = pd.concat([data1, data2], axis=1).sort_values(['qty_diff', 'turn_diff'], ascending=[False, False])
        prod_data = {'increased_prod': data[data['qty_diff']>0][:5].reset_index().to_dict(orient='records'),
                     'decreased_prod': data[data['qty_diff']<0][-5:].reset_index().to_dict(orient='records')}

        return prod_data