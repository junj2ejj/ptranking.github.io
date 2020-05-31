#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by Hai-Tao Yu | 2019/07/18 | https://y-research.github.io

"""Description

"""

import torch

from scipy import stats

from org.archive.metric.adhoc_metric import torch_ap_at_ks, torch_nDCG_at_ks, torch_kendall_tau, torch_nerr_at_ks


def test_ap():
    ''' todo-as-note: the denominator should be carefully checked when using AP@k '''
    # here we assume that there five relevant documents, but the system just retrieves three of them
    sys_sorted_labels = torch.Tensor([1.0, 0.0, 1.0, 0.0, 1.0])
    std_sorted_labels = torch.Tensor([1.0, 1.0, 1.0, 1.0, 1.0])
    ap_at_ks = torch_ap_at_ks(sys_sorted_labels, std_sorted_labels, ks=[1, 3, 5])
    print(ap_at_ks) # tensor([1.0000, 0.5556, 0.4533])

    sys_sorted_labels = torch.Tensor([1.0, 0.0, 1.0, 0.0, 1.0])
    std_sorted_labels = torch.Tensor([1.0, 1.0, 1.0, 0.0, 0.0])
    ap_at_ks = torch_ap_at_ks(sys_sorted_labels, std_sorted_labels, ks=[1, 3, 5])
    print(ap_at_ks)  # tensor([1.0000, 0.5556, 0.7556])

    # here we assume that there four relevant documents, the system just retrieves four of them
    sys_sorted_labels = torch.Tensor([1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0])
    std_sorted_labels = torch.Tensor([1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0])
    ap_at_ks = torch_ap_at_ks(sys_sorted_labels, std_sorted_labels, ks=[1, 2, 3, 5, 7])
    print(ap_at_ks) # tensor([1.0000, 1.0000, 0.6667, 0.6875, 0.8304])


def test_ndcg():
    sys_sorted_labels = torch.Tensor([1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0])
    std_sorted_labels = torch.Tensor([1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0])
    ndcg_at_ks = torch_nDCG_at_ks(sys_sorted_labels, std_sorted_labels, ks=[1, 2, 3, 4, 5, 6, 7])
    print(ndcg_at_ks) # tensor([1.0000, 1.0000, 0.7654, 0.8048, 0.8048, 0.8048, 0.9349])



def test_nerr():
    sys_sorted_labels = torch.Tensor([3.0, 2.0, 4.0])
    std_sorted_labels = torch.Tensor([4.0, 3.0, 2.0])
    nerr_at_ks = torch_nerr_at_ks(sys_sorted_labels, std_sorted_labels, ks=[1, 2, 3])
    print(nerr_at_ks)  # tensor([0.4667, 0.5154, 0.6640])



def test_kendall_tau():
    reference = torch.Tensor([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0])
    sys_1     = torch.Tensor([2.0, 1.0, 5.0, 3.0, 4.0, 6.0, 7.0, 9.0, 8.0, 10.0])
    sys_2     = torch.Tensor([10.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 1.0])

    tau_1 = torch_kendall_tau(sys_1, natural_ascending_as_reference=True)
    print('tau_1', tau_1)

    tau_2 = torch_kendall_tau(sys_2, natural_ascending_as_reference=True)
    print('tau_2', tau_2)

    tau, p = stats.kendalltau(reference.data.data.numpy(), sys_1)
    print('scipy-1', tau, p)

    tau, p = stats.kendalltau(reference.data.numpy(), sys_2)
    print('scipy-2', tau, p)

    print()
    print('-----------------------')


    res_reference, _ = torch.sort(reference, dim=0, descending=True)

    tau_1 = torch_kendall_tau(sys_1, natural_ascending_as_reference=False)
    print('tau_1', tau_1)

    tau_2 = torch_kendall_tau(sys_2, natural_ascending_as_reference=False)
    print('tau_2', tau_2)

    tau, p = stats.kendalltau(res_reference.data.numpy(), sys_1)
    print('scipy-1', tau, p)

    tau, p = stats.kendalltau(res_reference.data.numpy(), sys_2)
    print('scipy-2', tau, p)


if __name__ == '__main__':

    #1
    #test_ap()

    #2
    test_nerr()

    #3
    #test_kendall_tau()





