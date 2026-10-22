local meta = {}

function Meta(m)
  meta = m
end

local function text(value, fallback)
  if value == nil then
    return fallback or ""
  end
  return pandoc.utils.stringify(value)
end

local function render_inline_content(content, format)
  local doc = pandoc.Pandoc(content)
  if format == "html" then
    return pandoc.write(doc, format, {html_math_method = "mathjax"})
  end
  return pandoc.write(doc, format)
end

local function box_titles(kind)
  local labels = {
    intuition = "Intuition",
    blackboard = "Alice's notebook",
    oxford = "A glimpse of Oxford",
    trythis = "Try this at home",
    prooflight = "A gentle proof",
    hint = "Hint",
    answer = "Answer"
  }
  return labels[kind] or kind
end

function Div(el)
  local kind = el.classes[1]

  if kind == "intuition" or
     kind == "blackboard" or
     kind == "oxford" or
     kind == "trythis" or
     kind == "prooflight" then
    local body_html = render_inline_content(el.content, "html")
    local body_tex = render_inline_content(el.content, "latex")

    if FORMAT:match("latex") then
      local answer_note = kind == "trythis" and
        "\n\n\\small\\emph{Hints and answers appear at the back of the book.}" or ""
      return pandoc.RawBlock(
        "latex",
        "\\begin{" .. kind .. "box}\n" ..
        body_tex ..
        answer_note ..
        "\n\\end{" .. kind .. "box}"
      )
    end

    if FORMAT:match("html") then
      local answer_link = kind == "trythis" and
        '<p class="box-links"><a href="' .. text(meta.base_path, "/") .. 'answers/">Hints and answers</a></p>' or ""
      return pandoc.RawBlock(
        "html",
        '<aside class="box box-' .. kind .. '">' ..
        '<h3><span class="box-icon" aria-hidden="true"></span>' ..
        box_titles(kind) ..
        '</h3>' ..
        body_html ..
        answer_link ..
        '</aside>'
      )
    end
  end

  if kind == "hint" or kind == "answer" then
    local label = box_titles(kind)
    local body_html = render_inline_content(el.content, "html")
    local body_tex = render_inline_content(el.content, "latex")

    if FORMAT:match("latex") then
      return pandoc.RawBlock(
        "latex",
        "\\begin{" .. kind .. "box}\n" ..
        body_tex ..
        "\n\\end{" .. kind .. "box}"
      )
    end

    if FORMAT:match("html") then
      return pandoc.RawBlock(
        "html",
        '<details class="box box-' .. kind .. '">' ..
        '<summary>' .. label .. '</summary>' ..
        '<div class="box-body">' ..
        body_html ..
        '</div></details>'
      )
    end
  end

  if kind == "demo" then
    local demo_id = el.identifier
    if demo_id == nil or demo_id == "" then
      demo_id = el.attributes.id or ""
    end
    local demo_title = el.attributes.title or "Interactive demo"
    local base_path = text(meta.base_path, "/")
    local base_url = text(meta.base_url, "")
    local href = base_path .. "demos/" .. demo_id .. "/"
    local absolute_url = base_url .. "demos/" .. demo_id .. "/"
    local body_html = render_inline_content(el.content, "html")
    local body_tex = render_inline_content(el.content, "latex")

    if FORMAT:match("latex") then
      return pandoc.RawBlock(
        "latex",
        "\\begin{demobox}{" ..
        demo_title ..
        "}{" ..
        absolute_url ..
        "}{assets/qr/" ..
        demo_id ..
        ".png}\n" ..
        body_tex ..
        "\n\\end{demobox}"
      )
    end

    if FORMAT:match("html") then
      return pandoc.RawBlock(
        "html",
        '<aside class="demo-card" data-demo="' .. demo_id .. '">' ..
        '<div class="demo-card-inner">' ..
        '<p class="demo-eyebrow">Interactive demo</p>' ..
        '<h3>' .. demo_title .. '</h3>' ..
        body_html ..
        '<p><a class="button" href="' .. href .. '">Open the interactive demo</a></p>' ..
        '</div>' ..
        '</aside>'
      )
    end
  end

  return nil
end

function Image(el)
  if FORMAT:match("html") and el.src then
    local base_path = text(meta.base_path, "/")
    if el.src:sub(1, 8) == "/assets/" then
      el.src = base_path .. el.src:sub(2)
    elseif el.src:sub(1, 7) == "assets/" then
      el.src = base_path .. el.src
    end
  elseif FORMAT:match("latex") and el.src then
    if el.src:sub(-4) == ".svg" then
      el.src = el.src:sub(1, -5) .. ".pdf"
    end
    el.attributes.height = "50%"
  end
  return el
end

function Figure(el)
  if FORMAT:match("latex") then
    -- Keep a teaching diagram at its point of explanation.
    local rendered = pandoc.write(pandoc.Pandoc({el}), "latex")
    rendered = rendered:gsub("\\begin{figure}", "\\begin{figure}[H]", 1)
    return pandoc.RawBlock("latex", rendered)
  end
end

local function keep_chapter_notes(doc)
  if FORMAT:match("latex") then
    for index, block in ipairs(doc.blocks) do
      if block.t == "Header" and block.level == 2 and
         pandoc.utils.stringify(block.content):match("notes$") then
        -- Each chapter ends with a short recap and Alice's closing scene.
        -- Keep that recap together instead of leaving its final item alone.
        doc.blocks:insert(index, pandoc.RawBlock("latex",
          "\\par\\noindent\\begin{minipage}{\\linewidth}"))
        doc.blocks:insert(pandoc.RawBlock("latex", "\\end{minipage}\\par"))
        break
      end
    end
  end
  return doc
end

-- Read document metadata before rendering boxes and resolving asset URLs.
return {
  {Meta = Meta},
  {Image = Image, Div = Div, Figure = Figure},
  {Pandoc = keep_chapter_notes}
}
