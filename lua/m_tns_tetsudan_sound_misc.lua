-- include sfx 0 "m_tns_tetsudan_misc_brake_1.ogg"
-- include sfx 1 "m_tns_tetsudan_misc_stop_1.ogg"

IS_LOOP = {true, false}

FADE_OUT = 30
RADIUS_INNER = 10
RADIUS_OUTER = 150

local sfx_channel = {}
local sfx_volume = {}
local channels_not_in_use, channels_in_use = {0, 1, 2, 3}, {}

local function stop_channel(channel)
    if component.sfxStop(channel) then
        for i, v in ipairs(channels_in_use) do
            if v == channel then
                table.remove(channels_in_use, i)
                table.insert(channels_not_in_use, channel)
                return true
            end
        end
    end
    return false
end

local function allocate_channel()
    if #channels_not_in_use == 0 then
        stop_channel(channels_in_use[1])
    end
    if #channels_not_in_use > 0 then
        local channel = table.remove(channels_not_in_use, 1)
        table.insert(channels_in_use, channel)
        return channel
    else
        return nil
    end
end

function onTick()
    local composite, success = component.getInputLogicSlotComposite(0)
    if success then
        local bv = composite.bool_values
        for i = 1, #IS_LOOP do
            if bv[i] then
                sfx_volume[i] = 1
            elseif IS_LOOP[i] then
                sfx_volume[i] = math.max(sfx_volume[i] - 1 / FADE_OUT, 0)
            else
                sfx_volume[i] = 0
            end

            if bv[i] and sfx_channel[i] == nil then
                local channel = allocate_channel()
                if channel ~= nil then
                    local fn = IS_LOOP[i] and component.sfxPlayLoop or component.sfxPlayOnce
                    if fn(channel, i - 1, 0, 0, 0, RADIUS_INNER, RADIUS_OUTER, 1, 1, 1) then
                        sfx_channel[i] = channel
                    end
                end
            elseif not bv[i] and sfx_channel[i] ~= nil then
                if sfx_volume[i] <= 0 then
                    if stop_channel(sfx_channel[i]) then
                        sfx_channel[i] = nil
                    end
                else
                    component.sfxUpdate(sfx_channel[i], 0, 0, 0, RADIUS_INNER, RADIUS_OUTER, sfx_volume[i], 1)
                end
            end
        end
    end
end

function onRemoveFromSimulation()
    for i = 0, 3 do
        component.sfxStop(i)
    end
end

