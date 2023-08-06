# -*- coding: utf-8 -*-
import abc
from math import sqrt
import random
import time
from hepdata_converter.writers.array_writer import ArrayWriter, ObjectWrapper, ObjectFactory
import rootpy.io
import rootpy.ROOT
import numpy

__author__ = 'Michał Szostak'


class THFRootClass(ObjectWrapper):
    __metaclass__ = abc.ABCMeta

    _hist_classes = [rootpy.ROOT.TH1F, rootpy.ROOT.TH2F, rootpy.ROOT.TH3F]
    _hist_axes_names = ['x', 'y', 'z']
    dim = 0

    @classmethod
    def match(cls, independent_variables_map, dependent_variable):
        if not ObjectWrapper.match(independent_variables_map, dependent_variable):
            return False
        elif len(independent_variables_map) == cls.dim:
            for independent_variable in independent_variables_map:
                if 'high' not in independent_variable['values'][0]:
                    break
            else:
                return True
        elif cls.dim == 1 and 'high' in independent_variables_map[0]['values'][0]:
            return True
        return False

    def _create_hist(self, xval):

        name = "Hist%s_" % self.dim
        args = []

        for i in xrange(self.dim):
            args.append(len(xval[i]) - 1)
            args.append(numpy.array(xval[i], dtype=float))

            name += self.sanitize_name(self.independent_variables[0]['header']['name']) + "__"

        name += self.sanitize_name(self.dependent_variable['header']['name'])

        hist = self._hist_classes[self.dim - 1](name, '', *args)

        for i in xrange(self.dim):
            getattr(hist, self._hist_axes_names[i] + 'axis').title = self.independent_variables[i]['header']['name']

        if self.dim < len(self._hist_classes):
            getattr(hist, self._hist_axes_names[self.dim] + 'axis').title = self.dependent_variable['header']['name']

        for i in xrange(len(self.xval[0])):
            hist.fill(*([self.xval[dim_i][i] for dim_i in xrange(self.dim)] + [self.yval[i]]))
        return hist

    def create_object(self):
        self.calculate_total_errors()

        for i in xrange(self.dim):
            self.independent_variable_map.pop(0)

        xval = []

        for i in xrange(self.dim):
            xval.append([])
            i_var = self.independent_variables[i]['values']
            for x in i_var:
                xval[i].append(x['low'])
            xval[i].append(i_var[-1]['high'])

        hist = self._create_hist(xval)

        return hist


class TH3FRootClass(THFRootClass):
    dim = 3


class TH2FRootClass(THFRootClass):
    dim = 2


class TH1FRootClass(THFRootClass):
    dim = 1


class TGraph2DErrorsClass(ObjectWrapper):

    @classmethod
    def match(cls, independent_variables_map, dependent_variable):
        if not super(TGraph2DErrorsClass, cls).match(independent_variables_map, dependent_variable):
            return False
        if len(independent_variables_map) == 2 and cls.is_value_var(independent_variables_map[0]) and cls.is_value_var(independent_variables_map[1]):
            return True
        return False

    def create_object(self):
        self.calculate_total_errors()

        self.independent_variable_map.pop(0)
        self.independent_variable_map.pop(0)

        graph = rootpy.ROOT.TGraph2DErrors(len(self.xval[0]),
                                           numpy.array(self.xval[0], dtype=float),
                                           numpy.array(self.xval[1], dtype=float),
                                           numpy.array(self.yval, dtype=float),
                                           numpy.array(self.xerr_plus[0], dtype=float),
                                           numpy.array(self.xerr_plus[1], dtype=float),
                                           numpy.array(self.yerr_plus, dtype=float))

        graph.title = "Graph2D__%s__%s__%s" % (self.sanitize_name(self.independent_variables[0]['header']['name']),
                                               self.sanitize_name(self.independent_variables[1]['header']['name']),
                                               self.sanitize_name(self.dependent_variable['header']['name']))

        graph.xaxis.title = self.independent_variables[0]['header']['name']
        graph.yaxis.title = self.independent_variables[1]['header']['name']
        graph.zaxis.title = self.dependent_variable['header']['name']

        return graph


class TGraphAsymmErrorsRootClass(ObjectWrapper):
    def create_object(self):
        self.calculate_total_errors()

        self.independent_variable_map.pop(0)

        graph = rootpy.ROOT.TGraphAsymmErrors(len(self.xval[0]),
                                              numpy.array(self.xval[0], dtype=float),
                                              numpy.array(self.yval, dtype=float),
                                              numpy.array(self.xerr_minus[0], dtype=float),
                                              numpy.array(self.xerr_plus[0], dtype=float),
                                              numpy.array(self.yerr_minus, dtype=float),
                                              numpy.array(self.yerr_plus, dtype=float))

        graph.title = "Graph1D__%s__%s" % (self.sanitize_name(self.independent_variables[0]['header']['name']),
                                           self.sanitize_name(self.dependent_variable['header']['name']))

        graph.xaxis.title = self.independent_variables[0]['header']['name']
        graph.yaxis.title = self.dependent_variable['header']['name']

        return graph


class ROOT(ArrayWriter):
    help = 'Writes to ROOT format (binary) converts tables into files containing TH1 objects'
    class_list = [TH3FRootClass, TH2FRootClass, TH1FRootClass, TGraph2DErrorsClass, TGraphAsymmErrorsRootClass]

    def __init__(self, *args, **kwargs):
        super(ROOT, self).__init__(*args, **kwargs)
        self.extension = 'root'

    def _write_table(self, data_out, table):
        data_out.mkdir(table.name)
        data_out.cd(table.name)

        f = ObjectFactory(self.class_list, table.independent_variables, table.dependent_variables)
        for graph in f.get_next_object():
            graph.title = table.name
            graph.write()

    def _prepare_outputs(self, data_out, outputs):
        if isinstance(data_out, str) or isinstance(data_out, unicode):
            self.file_emulation = True
            outputs.append(rootpy.io.root_open(data_out, 'w'))
        # multiple tables - require directory
        elif isinstance(data_out, rootpy.ROOT.TFile):
            outputs.append(data_out)
        else: # assume it's a file like object
            self.file_emulation = True
            outputs.append(rootpy.io.TemporaryFile())

    def write(self, data_in, data_out, *args, **kwargs):
        """

        :param data_in:
        :type data_in: hepconverter.parsers.ParsedData
        :param data_out: filelike object
        :type data_out: file
        :param args:
        :param kwargs:
        """
        self._get_tables(data_in)

        self.file_emulation = False
        outputs = []
        self._prepare_outputs(data_out, outputs)
        output = outputs[0]

        for i in xrange(len(self.tables)):
            table = self.tables[i]

            self._write_table(output, table)

        if data_out != output and hasattr(data_out, 'write'):
            output.flush()
            output.re_open('read')
            buff = bytearray(output.get_size())
            output.read_buffer(buff, output.get_size())
            data_out.write(buff)

        if self.file_emulation:
            output.close()