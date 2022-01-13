=begin

MySQL And Python Billing
Copyright (C) 2021 Devisha Padmaperuma

MySQL And Python Billing is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

MySQL And Python Billing is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with MySQL And Python Billing.  If not, see <https://www.gnu.org/licenses/>.

=end

require 'asciidoctor'

def create
  Asciidoctor.convert_file './main.adoc', to_file: true, safe: :safe
  Asciidoctor.convert_file './log.adoc', to_file: true, safe: :safe
  Asciidoctor.convert_file './scenarios.adoc', to_file: true, safe: :safe
  Asciidoctor.convert_file './functions.adoc', to_file: true, safe: :safe
end

def clean
  File.delete "./main.html" if File.exist? "./main.html"
  File.delete "./log.html" if File.exist? "./log.html"
  File.delete "./scenarios.html" if File.exist? "./scenarios.html"
  File.delete "./functions.html" if File.exist? "./functions.html"
end

if ARGV[0] == "create"
  create
elsif ARGV[0] == "clean"
  clean
else
  puts 'ruby generate.rb  [create|clean]' \
    '' \
    'create:'\
      'generates the HTML file'\
      ''\
    'clean:'\
      'deletes the HTML files'
end