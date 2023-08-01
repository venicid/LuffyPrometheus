#!/usr/bin/env bash

hn="k8s-master01"
hostnamectl set-hostname $hn

systemctl stop firewalld
systemctl disable firewalld
systemctl status firewalld

setenforce 0
sed -i '/^SELINUX/s/enforcing/disabled/' /etc/selinux/config
getenforce
yum -y install lrzsz  yum-utils wget

mkdir /tmp/yum_repo_bk
/bin/mv -f /etc/yum.repos.d/* /tmp/yum_repo_bk
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
wget  -O /etc/yum.repos.d/epel-7.repo https://mirrors.aliyun.com/repo/epel-7.repo


mkdir -pv /opt/tgzs
mkdir -pv /opt/app
