#
# Cookbook Name:: sysctl
# Provider:: sysctl
# Author:: Guilhem Lettron <guilhem.lettron@youscribe.com>
#
# Copyright 2012, Societe Publica.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
action :save do

  fullname = get_path

  execute "sysctl-p" do
    command "sysctl -p #{fullname}"
    action :nothing
  end

  file get_path do
    notifies :run, "execute[sysctl-p]"
    content "#{get_variable} = #{new_resource.value}\n"
    owner 'root'
    group 'root'
    mode '0644'
  end
  new_resource.updated_by_last_action(true)
end


action :set do
  execute 'set sysctl' do
    command "sysctl #{get_variable}=#{new_resource.value}"
  end
  new_resource.updated_by_last_action(true)
end


action :remove do
  file get_path do
    action :delete
  end
  new_resource.updated_by_last_action(true)
end


def get_path
  f_name = new_resource.name.gsub(' ', '_')
  priority = new_resource.priority
  return new_resource.path ? new_resource.path : \
    "/etc/sysctl.d/#{priority}-#{f_name}.conf"
end


def get_variable
  return new_resource.variable ? new_resource.variable : new_resource.name
end
