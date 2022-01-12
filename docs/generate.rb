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