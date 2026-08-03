-- for development:
local p = quarto.log.warning

---Format string like in bash or python,
---e.g. f('Hello ${one}', {one = 'world'})
---@param s string The string to format
---@param kwargs {[string]: string} A table with key-value replacemen pairs
---@return string
local function f(s, kwargs)
  return (s:gsub('($%b{})', function(w) return kwargs[w:sub(3, -2)] or w end))
end


---Merge user provided options with defaults
---@param userOptions table
---@return string JSON string to pass to molstar
local function mergeOptions(url, userOptions)
  local defaultOptions = {
    text = url,
    width = 128,
    height = 128,
    colorDark = "#000000",
    colorLight = "#ffffff",
  }
  if userOptions == nil then
    return quarto.json.encode(defaultOptions)
  end

  for k, v in pairs(userOptions) do
    local value = pandoc.utils.stringify(v)
    if value == 'true' then value = true end
    if value == 'false' then value = false end
    defaultOptions[k] = value
  end

  return quarto.json.encode(defaultOptions)
end


---@return string
local function wrapInlineDiv(options)
  return [[
<div id="${id}" class="qrcode"></div>
<script type="text/javascript">
(function() {
  var script = document.currentScript;
  var qrcode = script.previousElementSibling;
  qrcode.qrcode = new QRCode(qrcode, ]] .. options .. [[);
  script.remove();
})();
</script>
    ]]
end

---@return string
local function wrapInlineTex(url, opts)
  return [[
\qrcode[]] .. opts .. [[]{]] .. url .. [[}
    ]]
end

return {
  ['qrcode'] = function(args, kwargs, _)
    if quarto.doc.is_format("html:js") then
      quarto.doc.add_html_dependency {
        name = 'qrcodejs',
        version = 'v1.0.0',
        scripts = { './assets/qrcode.js' },
      }
      local url = pandoc.utils.stringify(args[1])
      local id = ""
      if args[2] ~= nil then
        id = f('id="${id}" ', { id = pandoc.utils.stringify(id) })
      end
      local options = mergeOptions(url, kwargs)
      local text = wrapInlineDiv(options)
      return pandoc.RawBlock(
        'html',
        f(text, { id = id })
      )
    elseif quarto.doc.is_format("pdf") then
      quarto.doc.use_latex_package("qrcode")
      local url = pandoc.utils.stringify(args[1])
      local opts = ""
      for k, v in pairs(kwargs) do
        if string.match(k, "^pdf") then
          k = string.sub(k, 4)
          opts = opts .. k .. "=" .. v .. ", "
        end
      end
      for _, v in ipairs(args) do
        if string.match(v, "^pdf") then
          v = string.sub(v, 4)
          opts = opts .. v .. ", "
        end
      end
      if string.len(opts) then
        opts = string.sub(opts, 1, string.len(opts) - 2)
      end
      local text = wrapInlineTex(url, opts)
      return pandoc.RawBlock(
        'tex',
        text
      )
    end
  end,
}
